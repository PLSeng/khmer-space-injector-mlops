import pytest
from fastapi.testclient import TestClient

# Adjust this import if your app entrypoint is different
from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
