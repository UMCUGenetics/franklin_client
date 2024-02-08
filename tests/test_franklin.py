import os
import franklin_client

franklin = franklin_client.Franklin(
    base_uri=os.environ['POSTMAN_FRANKLIN_MOCKUP_URI'],
    email='py@test.nl',
    password='pytest'
)


def test_get_assay_list():
    assert franklin.get_assay_list() == [
        {"id": "7606dc0q-2e93-4967-9e4b-db85b128c5da", "name": "Exome"},
        {"id": "bd0bf7eb-557d-4581-bc76-6bcef59a355a", "name": "Panel"}
    ]

