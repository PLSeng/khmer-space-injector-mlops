import json
from pathlib import Path
import pytest

from app.services.artifacts import load_vocab
from app.core.config import settings


def test_load_vocab(tmp_path: Path):
    vocab_path = tmp_path / "vocab.json"
    vocab_path.write_text(json.dumps({"a": 1, "<UNK>": 2}), encoding="utf-8")

    vocab = load_vocab(vocab_path)
    assert vocab["a"] == 1
    assert "<UNK>" in vocab


@pytest.mark.integration
def test_artifact_files_exist():
    artifact_path = settings.artifact_path
    required = ["checkpoint.pt", "config.json", "vocab.json"]

    missing = [f for f in required if not (artifact_path / f).is_file()]
    if missing:
        pytest.skip(f"Missing artifacts in {artifact_path}: {missing}")

    for f in required:
        assert (artifact_path / f).is_file()