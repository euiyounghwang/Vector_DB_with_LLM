import pytest
from fastapi import FastAPI # type: ignore
from fastapi.testclient import TestClient # type: ignore
from main import app

# In order to share fixtures across multiple test files, pytest suggests defining fixtures in a conftest.py

@pytest.fixture(scope="class")
def mock_client():
    # app = FastAPI()
    client = TestClient(app)
    
    return client
