def get_file_name_from_aws_url(aws_url):
    """Get file name from AWS URL

    Args:
        aws_url (str): URL to file on AWS

    Returns:
        str: File name
    """
    return aws_url.split("?")[0].split("/")[-1]


def get_file_name_from_headers(response_headers):
    """Get file name from response headers

    Args:
        response_headers (dict): response headers

    Returns:
        str: File name
    """
    content_disposition = response_headers.get("Content-Disposition")
    if content_disposition:
        parts = content_disposition.split(";")
        for part in parts:
            part = part.strip()
            if part.startswith("filename="):
                return part.split("=")[1].strip('"')
    return None
