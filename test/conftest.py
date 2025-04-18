import os
import pytest
from fastapi.testclient import TestClient
from server.main import app


@pytest.fixture(scope="session", autouse=True)
def enable_test_mode():
    os.environ["TESTING"] = "1"


@pytest.fixture
def client():
    return TestClient(app)
