import argparse
from .core import miscan_main


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vcf', type=str, help='The VCF file')
    parser.add_argument('-o', type=str, help='result folder')
    parser.add_argument('--weight', type=str, default='', help='weight folder')
    args = parser.parse_args()

    miscan_main(args.o, args.vcf, args.weight)
