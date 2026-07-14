from typing_extensions import Literal

import typer

from franklin_client.config import settings
from franklin_client.services import Franklin
from franklin_client.utils import get_file_name_from_aws_url, download_file

# Configure Typer CLI
app = typer.Typer(no_args_is_help=True)
analysis_app = typer.Typer(no_args_is_help=True)
assay_app = typer.Typer(no_args_is_help=True)

app.add_typer(analysis_app, name="analysis", help="Get analysis information from Franklin")
app.add_typer(assay_app, name="assay", help="Get assay information from Franklin")


@analysis_app.command("search")
def analysis_search(name: str):
    """Search for an analysis by name

    Args:
        name (str): Analysis name
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())
    analyses = franklin.get_analyses(analysis_name=name)

    typer.echo("ID\tName\tAssay ID")
    for analysis in analyses:
        typer.echo(f"{analysis['id']}\t{analysis['name']}\t{analysis['assay_id']}")


@analysis_app.command("view")
def analysis_view(analysis_id: int):
    """View analysis information from Franklin

    Args:
        analysis_id (int): Analysis id
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())
    analysis = franklin.get_analysis(analysis_id)

    typer.echo(f"ID: {analysis['id']}")
    typer.echo(f"Name: {analysis['name']}")
    typer.echo(f"Assay ID: {analysis['assay_uuid']}")
    typer.echo(f"Status: {analysis['status_description']}")

    typer.echo("Samples:")
    for sample in analysis["samples"]:
        typer.echo(f"  - {sample['sample_name']}")


@analysis_app.command("download_bam")
def analysis_download_bam(analysis_id: int):
    """Download BAM file from Franklin

    Args:
        analysis_id (int): Analysis id
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())

    for file_type, file_url in franklin.get_analysis_bam(analysis_id).items():
        file_name = get_file_name_from_aws_url(file_url)
        download_file(file_url, file_name)


@analysis_app.command("download_coverage_report")
def analysis_download_coverage_report(
    analysis_id: int,
    coverage_type: Literal["genes", "exons", "kit"] = "genes",
    coverage_region: Literal["coding", "targeted"] = "coding",
    virtual_panel_id: str = "",
):
    """Download coverage report from Franklin

    Args:
        analysis_id (int): Analysis id
        coverage_type (str, optional): Coverage type. Defaults to "genes".
        coverage_region (str, optional): Coverage region. Defaults to "coding".
        virtual_panel_ids (list[str], optional):
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())
    coverage_report = franklin.get_analysis_coverage_report(
        analysis_id, coverage_type=coverage_type, coverage_region=coverage_region, virtual_panel_ids=[virtual_panel_id]
    )
    download_file(coverage_report["download_url"])


@analysis_app.command("download_vcf")
def analysis_download_vcf(analysis_id: int):
    """Download VCF file from Franklin

    Args:
        analysis_id (int): Analysis id
    """

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())
    analysis_vcf_files = franklin.get_analysis_vcf(analysis_id)

    for file_type in analysis_vcf_files:
        for file_url in analysis_vcf_files[file_type]:
            file_name = get_file_name_from_aws_url(file_url)
            download_file(file_url, file_name)


@assay_app.command("list")
def assay_list():
    """List all assays from Franklin"""

    franklin = Franklin(settings.franklin.base_uri, settings.franklin.username, settings.franklin.password.get_secret_value())
    assays = franklin.get_assays()

    typer.echo("ID\tName")
    for assay in assays:
        typer.echo(f"{assay['id']}\t{assay['name']}")


if __name__ == "__main__":
    app()
