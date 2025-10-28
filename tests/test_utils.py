from franklin_client import utils


def test_get_file_name_from_aws_url():
    utils.get_file_name_from_aws_url(
        "https://server.amazonaws.com/path/to/bam/123__950-dragen-ready.bam?X-Amz-Algorithm=AWS4-HMAC-SHA256"
    ) == "123__950-dragen-ready.bam"


def test_get_file_name_from_headers():
    headers = {
        "Content-Disposition": 'attachment; filename="DN2025_00123_coverage_report.csv"',
        "Content-Type": "application/octet-stream",
    }
    assert utils.get_file_name_from_headers(headers) == "DN2025_00123_coverage_report.csv"
