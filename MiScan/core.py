# -*- coding: utf-8 -*-
import operator
import warnings
from collections import Counter
from os import environ, makedirs
from os import system, popen
from os.path import join, exists
import re

import keras.backend as K
import matplotlib as mpl
import numpy as np
import pandas as pd
from scipy.io import mmread
import shutil

from .logging import get_logger
from .model import build_dense_model as build_model
from .utils import get_data, exists_or_mkdir

mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from matplotlib.transforms import Bbox

warnings.filterwarnings("ignore")
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams["font.sans-serif"] = "Arial"
environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logger = get_logger(__name__)


def vcf_to_sparse(outDir, inFeaID, inFeaBed, inVcf, featureID):
    """
    convert the vcf to a feature matrix, `matrix.mtx`
    :param outDir: output directory
    :param inFeaID: `13885fea_exon_cut_100bp_2sample.txt` in dependency_data
    :param inFeaBed: `tcga_13885fea_exon_cut_100bp.bed` in dependency_data
    :param inVcf: the input vcf file path
    :param featureID: `featureID.bed` in dependency_data
    :return:
    """
    logger.info('start converting Vcf to feature matrix')
    exists_or_mkdir(outDir)
    sample_name = inVcf.split('/')[-1].split('.')[0]
    # --------------------------------------------------
    vcf_list = []
    with open(inVcf) as f:
        for line in f:
            if re.match('#', line):
                pass
            else:
                data = line.strip().split('\t')
                chrom = data[0] if re.match('chr', data[0]) else 'chr' + data[0]
                start = int(data[1])
                end = start + 1
                qual = data[5]
                alt = data[3] + ',' + data[4]
                vcf_list.append([chrom, start, end, 1, qual, alt])
    vcf_df = pd.DataFrame(vcf_list, columns=['chrom', 'start', 'end', 'sample_name', 'qual', 'alt'])
    vcf_df.sort_values(by=['chrom', 'start'], ascending=True, inplace=True)
    outSnpBedFile = join(outDir, 'snp_sampleID.bed')
    vcf_df.to_csv(outSnpBedFile, sep='\t', header=None, index=None)
    # --------------------------------------------------
    feature_ls = list(pd.read_table(inFeaID, names=['fea'])['fea'])
    nb_fea = len(feature_ls)
    sparDir = join(outDir, 'DataSparse')
    if not exists(sparDir):
        makedirs(sparDir)

    with open(join(sparDir, 'sample.tsv'), 'w') as output_sample:
        output_sample.write('%s\n' % sample_name)

    shutil.copyfile(inFeaID, join(sparDir, 'feature.tsv'))
    outFeaId = join(sparDir, 'featureID.bed')
    shutil.copyfile(featureID, outFeaId)

    # --------------------------------------------------------------------------------
    outSNVCoverWindow = join(outDir, 'window.snvCover.txt')
    tmpMtxCountFile = join(sparDir, 'tmpMtx.count.txt')
    out_testPat_mtx = join(sparDir, 'matrix.mtx')

    system("bedtools intersect -a {0} -b {1} -wo > {2}".format(inFeaBed, outSnpBedFile, outSNVCoverWindow))
    system(
        " bedtools intersect -a %s -b %s -wo | awk \'{print $4\"\t\"$8\"\t\"\'1\'}\' | sort -u | sort -k1,1n -k2,2n >  %s " % (
            outFeaId, outSnpBedFile, tmpMtxCountFile))
    nb_lines = int(popen('wc -l {0}'.format(tmpMtxCountFile)).read().strip().split(' ')[0])

    with open(out_testPat_mtx, 'a') as f:
        f.write('%%MatrixMarket matrix coordinate integer general\n%\n')
        f.write('{0}\t{1}\t{2}\n'.format(nb_fea, 1, nb_lines))
    system('cat {0} >> {1}'.format(tmpMtxCountFile, out_testPat_mtx))
    # --------------------------------------------------------------------------------


def prediction(outDir, model_weight):
    """
    predict single sample breast cancer risk

    :param outDir: output directory
    :param model_weight: the MiScan model weight file path
    :return: (risk_to_be_patient, probability_to_be_normal)

    """
    logger.info('start model evaluation')
    model = build_model()
    model.load_weights(model_weight)
    test_array = mmread('{0}/DataSparse/matrix.mtx'.format(outDir)).todense().T
    y_pred_ay = model.predict(test_array)
    y_pred_pat = y_pred_ay[0][1]
    y_pred_norm = y_pred_ay[0][0]
    K.clear_session()
    return y_pred_pat, y_pred_norm


def generate_report(inDir, outDir, y_pred_pat):
    """
    generate report for single sample, including Cancer Risk Prediction | Top Gene Mutation Sites

    :param inDir: for historical reason, actually, it's the path of `MISCAN.norm.trainPred.txt` and
    'MISCAN.pat.trainPred.txt' in dependency_data
    :param outDir: output directory
    :param y_pred_pat: risk_to_be_patient from func `prediction`
    :return:
    """
    logger.info('start generating report')
    fig, axes = plt.subplots(6, 1, figsize=(8, 8))
    axes[0].set_position(Bbox([[0.02, 0.4], [0.98, 0.93]]))
    # axes[0].set_title(r'$\underline{sin(x)}$', fontsize=30)
    axes[0].text(0.5, 1, 'Feedback Report', fontsize=30, ha='center', style='italic')
    # axes[0].text(0.5, 1, title, fontsize=30, ha='center', weight='bold')
    axes[0].axis('off')

    axes[5].set_position(Bbox([[0.02, 0.9], [0.98, 0.93]]))
    axes[5].set_xlim([0, 1])
    axes[5].plot([0.28, 0.72], [3, 3], color='black')
    axes[5].axis('off')

    axes[1].set_position(Bbox([[0.01, 0.8], [0.99, 0.88]]))
    axes[1].text(0.01, 0.72, '1. Breast cancer risk predicted by MiScan', fontsize=20)
    axes[1].axis('off')

    axes[2].set_position(Bbox([[0.09, 0.57], [0.95, 0.83]]))

    train_pat = pd.read_csv(inDir[0], header=None).values
    train_norm = pd.read_csv(inDir[1], header=None).values
    train_pat = np.squeeze(train_pat, axis=1)
    train_norm = np.squeeze(train_norm, axis=1)
    g = sns.kdeplot(train_pat, label='trainPat', ax=axes[2],
                    shade=True, color='#ffb7ce')
    g = sns.kdeplot(train_norm, label='trainNorm', ax=axes[2],
                    shade=True, color='#95d0fc')
    axes[2].set_xlabel('Cancer risk', size=15)
    axes[2].set_ylabel('Density', size=15)
    for tick in axes[2].xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in axes[2].yaxis.get_major_ticks():
        tick.label.set_fontsize(12)

    # axes[2].set_title('Distribution of probability by MiScan', size=20)
    axes[2].legend(loc='upper right', ncol=4, prop={'size': 12}, frameon=False)
    axes[2].vlines(y_pred_pat, ymin=0, ymax=50, linestyles='dashed', color='grey')
    axes[2].set_ylim([0, 60])
    axes[2].set_yticks(list(np.linspace(0, 60, 4)))
    gg = axes[2].scatter(y_pred_pat, 10, marker='o', s=50, color='#8e82fe', edgecolor='black', linewidth='0.5')
    gg.set_zorder(5)
    # texts = [axes[1].text(y_pred_pat-0.2, 40, 'Pred\n{0}'.format(y_pred_pat), size=20)]
    # texts = [axes[1].text(y_pred_pat - 0.2, 40, 'Pred\n{0}'.format(y_pred_pat), size=15)]
    if y_pred_pat > 0.5:
        x_text = y_pred_pat - 0.4
        y_text = 10 + 5
        xx = y_pred_pat - 0.02
        yy = 10 + 1
    else:
        x_text = y_pred_pat + 0.1
        y_text = 10 + 5
        xx = y_pred_pat + 0.02
        yy = 10 + 1
    if isinstance(y_pred_pat, int):
        axes[2].annotate(s='breast cancer risk:{0}'.format(y_pred_pat),
                         xytext=(x_text, y_text), xy=(xx, yy),
                         arrowprops=dict(arrowstyle="simple", relpos=(1, 0.5), color='#c5c9c7'),
                         size=15)
    else:
        axes[2].annotate(s='breast cancer risk:{:.3}'.format(y_pred_pat),
                         xytext=(x_text, y_text), xy=(xx, yy),
                         arrowprops=dict(arrowstyle="simple", relpos=(1, 0.5), color='#c5c9c7'),
                         size=15)

    axes[3].set_position(Bbox([[0.01, 0.4], [0.99, 0.5]]))
    axes[3].text(0.01, 0.52, '2. Genes ranked by the number of mutations', fontsize=20)
    axes[3].axis('off')

    # Fig 2
    axes[4].set_position(Bbox([[0.09, 0.1], [0.95, 0.42]]))
    inCoverSnv = join(outDir, 'window.snvCover.txt')
    geneMutantCount_dic = Counter([x.split('_')[0] for x in list(pd.read_table(inCoverSnv, header=None).iloc[:, 3])])
    sorted_xy = sorted(geneMutantCount_dic.items(), key=operator.itemgetter(1))
    sorted_xy.reverse()
    geneMutant_ls = []
    mutantCount_ls = []
    for xx, yy in sorted_xy:
        geneMutant_ls.append(xx)
        mutantCount_ls.append(yy)

    nb_plot = 100
    nb_show = 10

    axes[4].scatter(range(len(geneMutant_ls))[:nb_show], mutantCount_ls[:nb_show], s=12, marker='^', color='#0165fc',
                    label='Top {0} frequently mutated gene'.format(nb_show))
    axes[4].scatter(range(len(geneMutant_ls))[nb_show:nb_plot], mutantCount_ls[nb_show:nb_plot], s=12, marker='o', c='',
                    edgecolors='#a2cffe', label='Other mutated gene'.format(nb_show))
    axes[4].legend(loc='upper right')
    axes[4].set_xlabel('Ranked genes', fontsize=15, labelpad=10)
    axes[4].set_ylabel('The number of mutations', fontsize=15)
    for tick in axes[4].xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in axes[4].yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    texts = [axes[4].text(i, mutantCount_ls[i], geneMutant_ls[i], fontdict={'size': 8}) for i in range(nb_show)]
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='grey'), ax=axes[4])
    outFile = '{0}/Report.pdf'.format(outDir)
    plt.savefig(outFile, dpi=1000)
    plt.close()


def miscan_main(outDir, inVcf, model_weight=''):
    """
    website sanctuary analysis core callable func
    :param model_weight: path of model weights
    :param outDir: temp, final result dir
    :param inVcf:input vcf full absolute path
    :return:no return
    """

    dict_data = get_data()
    if not model_weight:
        raise FileNotFoundError('please config the weights path')
    in_dir = (dict_data['train_pat'], dict_data['train_norm'])

    vcf_to_sparse(outDir, dict_data['inFeaID'], dict_data['inFeaBed'], inVcf, dict_data['featureID'])
    y_pred_pat, _ = prediction(outDir, model_weight)
    generate_report(in_dir, outDir, 1)
