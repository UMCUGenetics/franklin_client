import os
import franklin_client

franklin = franklin_client.Franklin(
    base_uri=os.environ['FRANKLIN_BASE_URI'],
    username='pytest',
    password='pytest'
)


def test_get_assay_list():
    assert len(franklin.get_assay_list()) == 2
