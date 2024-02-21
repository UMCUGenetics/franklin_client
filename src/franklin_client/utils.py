def get_file_name_from_aws_url(aws_url):
    """Get file name from AWS URL

    Args:
        aws_url (str): URL to file on AWS

    Returns:
        str: File name
    """
    return aws_url.split('?')[0].split('/')[-1]
