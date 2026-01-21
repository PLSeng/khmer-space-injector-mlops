# tests/unit/test_segmenter.py
import pytest
from app.services.segmenter import Segmenter

class DummyModel:
    pass

def test_segment_strips_spaces_when_not_preserving(monkeypatch):
    seg = Segmenter(
        model=DummyModel(),
        vocab={"<UNK>": 1},
        device="cpu",
        max_len=128,
        unk_token="<UNK>",
        decode_insert_label=1,
        preserve_existing_spaces=False,
    )

    calls = []

    def fake_segment_no_spaces(x: str) -> str:
        calls.append(x)
        return f"[{x}]"

    monkeypatch.setattr(seg, "_segment_no_spaces", fake_segment_no_spaces)

    out = seg.segment(" a b ")
    assert out == "[ab]"
    assert calls == ["ab"]

def test_segment_preserve_existing_spaces(monkeypatch):
    seg = Segmenter(
        model=DummyModel(),
        vocab={"<UNK>": 1},
        device="cpu",
        max_len=128,
        unk_token="<UNK>",
        decode_insert_label=1,
        preserve_existing_spaces=True,
    )

    calls = []
    monkeypatch.setattr(seg, "_segment_no_spaces", lambda x: calls.append(x) or x.upper())

    out = seg.segment("aa bb")
    assert out == "AA BB"
    assert calls == ["aa", "bb"]
