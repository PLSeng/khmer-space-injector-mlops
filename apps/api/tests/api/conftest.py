# tests/api/conftest.py
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import deps

class DummyDB:
    def execute(self, *args, **kwargs):
        return None

def override_get_db():
    yield DummyDB()

@pytest.fixture()
def client():
    app.dependency_overrides[deps.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()