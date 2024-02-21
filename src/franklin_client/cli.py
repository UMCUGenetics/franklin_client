import argparse
import shutil

import requests

from franklin_client import Franklin
from franklin_client.utils import get_file_name_from_aws_url


def download_bam(args):
    """Download BAM file from Franklin

    Args:
        args (argparse): command line arguments
    """

    franklin = Franklin(args.base_uri, args.email, args.password)

    for file_type, file_url in franklin.get_analysis_bam(args.analysis_id).items():
        file_name = get_file_name_from_aws_url(file_url)

        with requests.get(file_url, stream=True) as r:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)


def download_vcf(args):
    """Download VCF file from Franklin

    Args:
        args (argparse): command line arguments
    """

    franklin = Franklin(args.base_uri, args.email, args.password)
    analysis_vcf_files = franklin.get_analysis_vcf(args.analysis_id)

    for file_type in analysis_vcf_files:
        for file_url in analysis_vcf_files[file_type]:
            file_name = get_file_name_from_aws_url(file_url)
            print(file_name, file_url)
            with requests.get(file_url, stream=True) as r:
                with open(file_name, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)


def main():
    """CLI entry point."""

    parser = argparse.ArgumentParser(description='Franklin API client interface')
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    franklin_connection_parser = argparse.ArgumentParser(add_help=False)
    franklin_connection_parser.add_argument('base_uri', help='Base uri for the Franklin server')
    franklin_connection_parser.add_argument('email', help='Franklin username')
    franklin_connection_parser.add_argument('password', help='Franklin password')

    parser_download_bam = subparsers.add_parser(
        'download_bam', parents=[franklin_connection_parser], help='Download analysis BAM file'
    )
    parser_download_bam.add_argument('analysis_id', type=int, help='Analysis id')
    parser_download_bam.set_defaults(func=download_bam)

    parser_download_vcf = subparsers.add_parser(
        'download_vcf', parents=[franklin_connection_parser], help='Download all analysis VCF files'
    )
    parser_download_vcf.add_argument('analysis_id', type=int, help='Analysis id')
    parser_download_vcf.set_defaults(func=download_vcf)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
