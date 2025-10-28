import os

import pytest
from dotenv import load_dotenv

from franklin_client.services import Franklin


@pytest.fixture(scope="session")
def franklin():
    load_dotenv()
    return Franklin(base_uri=os.environ["POSTMAN_FRANKLIN_MOCKUP_URI"], email="py@test.nl", password="pytest")
