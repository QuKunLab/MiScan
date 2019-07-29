from time import time
from pathlib import Path
HERE = Path(__file__).parent.parent


def time_it(func):
    """
    time record decorator

    :param func:
    :return: wrapper function, callable
    """
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        print('finished in %s' % (time() - start))
    return wrapper


def get_data():
    """
    get dependency data config

    :return: dict
    """
    return {
        'inFeaBed': HERE / 'dependency_data/tcga_13885fea_exon_cut_100bp.bed',
        'inFeaID': HERE / 'dependency_data/13885fea_exon_cut_100bp_2sample.txt',
        'train_pat': HERE / 'dependency_data/MISCAN.pat.trainPred.txt',
        'train_norm': HERE / 'dependency_data/MISCAN.norm.trainPred.txt',
        'featureID': HERE / 'dependency_data/featureID.bed'
    }
