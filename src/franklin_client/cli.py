import shutil
from typing_extensions import Literal

import requests
import typer

from franklin_client.config import settings
from franklin_client.services import Franklin
from franklin_client.utils import get_file_name_from_aws_url, get_file_name_from_headers

app = typer.Typer(no_args_is_help=True)


@app.command("download_bam")
def download_bam(analysis_id: int):
    """Download BAM file from Franklin

    Args:
        analysis_id (int): Analysis id
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())

    for file_type, file_url in franklin.get_analysis_bam(analysis_id).items():
        file_name = get_file_name_from_aws_url(file_url)

        with requests.get(file_url, stream=True) as r:
            with open(file_name, "wb") as f:
                shutil.copyfileobj(r.raw, f)


@app.command("download_coverage_report")
def download_coverage_report(
    analysis_id: int,
    coverage_type: Literal["genes", "exons", "kit"] = "genes",
    coverage_region: Literal["coding", "targeted"] = "coding",
):
    """Download coverage report from Franklin

    Args:
        analysis_id (int): Analysis id
        coverage_type (str, optional): Coverage type. Defaults to "genes".
        coverage_region (str, optional): Coverage region. Defaults to "coding".
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())
    coverage_report = franklin.get_analysis_coverage_report(
        analysis_id, coverage_type=coverage_type, coverage_region=coverage_region
    )
    file_url = coverage_report["download_url"]
    with requests.get(file_url, stream=True) as r:
        file_name = get_file_name_from_headers(r.headers)
        with open(file_name, "wb") as f:
            shutil.copyfileobj(r.raw, f)


@app.command("download_vcf")
def download_vcf(analysis_id: int):
    """Download VCF file from Franklin

    Args:
        analysis_id (int): Analysis id
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())
    analysis_vcf_files = franklin.get_analysis_vcf(analysis_id)

    for file_type in analysis_vcf_files:
        for file_url in analysis_vcf_files[file_type]:
            file_name = get_file_name_from_aws_url(file_url)
            with requests.get(file_url, stream=True) as r:
                with open(file_name, "wb") as f:
                    shutil.copyfileobj(r.raw, f)


if __name__ == "__main__":
    app()
