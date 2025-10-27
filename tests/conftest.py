import os

import pytest
from dotenv import load_dotenv

import franklin_client


@pytest.fixture(scope="session")
def franklin():
    load_dotenv()
    return franklin_client.Franklin(base_uri=os.environ["POSTMAN_FRANKLIN_MOCKUP_URI"], email="py@test.nl", password="pytest")
