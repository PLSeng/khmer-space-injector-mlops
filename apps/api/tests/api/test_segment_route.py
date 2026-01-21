# tests/api/test_segment_route.py
import app.api.routes.segment as segment_route

class FakeSegmenter:
    def segment(self, text: str) -> str:
        return "OUT:" + text

def test_segment_ok(client, monkeypatch):
    monkeypatch.setattr(segment_route, "_segmenter", FakeSegmenter())

    r = client.post("/api/segment", json={"text": "abc"})
    assert r.status_code == 200
    data = r.json()
    assert data["input"] == "abc"
    assert data["output"] == "OUT:abc"
