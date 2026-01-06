def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, dict)
    assert data.get("status") == "ok"
