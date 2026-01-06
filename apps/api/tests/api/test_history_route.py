def test_history_empty_or_ok(client):
    """
    History endpoint should:
    - return 200
    - return a list (possibly empty)
    """
    resp = client.get("/api/records")

    assert resp.status_code == 200
    data = resp.json()

    assert isinstance(data, list)


def test_history_after_segment_call(client):
    """
    Calling /api/segment should create a record
    retrievable via /api/records.
    """
    payload = {"text": "ខ្ញុំស្រលាញ់ភាសាខ្មែរ"}

    # Call segment first
    seg_resp = client.post("/api/segment", json=payload)
    assert seg_resp.status_code == 200

    # Fetch history
    hist_resp = client.get("/api/records")
    assert hist_resp.status_code == 200

    records = hist_resp.json()
    assert isinstance(records, list)
    assert len(records) >= 1

    record = records[-1]

    # Define the record contract now
    assert set(record.keys()) >= {
        "id",
        "input_text",
        "output_text",
        "created_at",
    }

    assert record["input_text"] == payload["text"]
    assert isinstance(record["output_text"], str)
