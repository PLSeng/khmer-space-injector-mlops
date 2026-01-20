import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.integration
def test_history_real_db():
    if not os.getenv("DATABASE_URL"):
        pytest.skip("DATABASE_URL not set")

    with TestClient(app) as client:
        r = client.get("/api/history")
        assert r.status_code == 200
        assert isinstance(r.json(), list)