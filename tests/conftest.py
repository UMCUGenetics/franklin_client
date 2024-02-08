import os

import pytest

import franklin_client


@pytest.fixture(scope="session")
def franklin():
    return franklin_client.Franklin(
        base_uri=os.environ['POSTMAN_FRANKLIN_MOCKUP_URI'],
        email='py@test.nl',
        password='pytest'
    )