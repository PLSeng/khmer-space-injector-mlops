import pytest


def test_segment_happy_path(client):
    payload = {"text": "ខ្ញុំស្រលាញ់ភាសាខ្មែរ"}  # example input
    resp = client.post("/api/segment", json=payload)

    assert resp.status_code == 200
    data = resp.json()

    # Contract (define it now so FE/BE don't drift)
    assert set(data.keys()) >= {"input", "output", "meta"}
    assert data["input"] == payload["text"]
    assert isinstance(data["output"], str)
    assert isinstance(data["meta"], dict)

    # meta fields are flexible, but these are common and useful
    # (you can delete these assertions if you don't want them)
    for k in ["model", "latency_ms"]:
        if k in data["meta"]:
            assert data["meta"][k] is not None


@pytest.mark.parametrize("bad_payload", [
    {},  # missing text
    {"text": ""},  # empty
    {"text": "   "},  # whitespace-only (you may choose to treat as invalid)
])
def test_segment_invalid_input(client, bad_payload):
    resp = client.post("/api/segment", json=bad_payload)

    # Choose ONE behavior and keep it consistent:
    # - 422 if you validate with Pydantic (recommended)
    # - 400 if you manually validate
    assert resp.status_code in (400, 422)


def test_segment_rejects_non_json(client):
    resp = client.post(
        "/api/segment",
        data="text=hello",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code in (400, 415, 422)
