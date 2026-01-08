import json
from pathlib import Path
from typing import Dict, Any

def load_json(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def load_vocab(vocab_path: Path) -> Dict[str, int]:
    vocab = load_json(vocab_path)
    if not isinstance(vocab, dict):
        raise ValueError("vocab.json must be a dict[str,int]")
    return {str(k): int(v) for k, v in vocab.items()}
