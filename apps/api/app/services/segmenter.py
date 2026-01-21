# apps/api/app/services/segmenter.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any
import json
import unicodedata

import torch

from app.core.config import settings
from app.services.artifacts import load_vocab
from app.services.utils import decode_spaces
from app.services.net import KhmerRNN

def chunk_text(text: str, max_len: int) -> List[str]:
    return [text[i : i + max_len] for i in range(0, len(text), max_len)]

def _load_config(config_path: Path) -> Dict[str, Any]:
    if not config_path.is_file():
        raise FileNotFoundError(f"Missing config.json: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def _preprocess(text: str, cfg: Dict[str, Any]) -> str:
    p = cfg.get("preprocess", {})  # :contentReference[oaicite:1]{index=1}
    if text is None:
        return ""

    # unicode normalization (e.g., NFC)
    norm = p.get("normalize_unicode")
    if norm:
        text = unicodedata.normalize(norm, text)

    if p.get("strip", True):
        text = text.strip()

    if p.get("lowercase", False):
        text = text.lower()

    # collapse all whitespace runs -> single spaces
    if p.get("collapse_spaces", False):
        text = " ".join(text.split())

    return text


@dataclass
class Segmenter:
    model: KhmerRNN
    vocab: Dict[str, int]
    device: str
    max_len: int
    unk_token: str
    decode_insert_label: int
    preserve_existing_spaces: bool

    @classmethod
    def load_from_artifacts(cls, artifact_dir: Path, device: str | None = None) -> "Segmenter":
        # Files
        config_path = artifact_dir / "config.json"
        vocab_path = artifact_dir / "vocab.json"
        ckpt_path = artifact_dir / "checkpoint.pt"

        cfg = _load_config(config_path)

        # Runtime knobs :contentReference[oaicite:2]{index=2}
        runtime = cfg.get("runtime", {})
        torch_threads = int(runtime.get("torch_num_threads", 1))
        torch.set_num_threads(torch_threads)

        if device is None:
            device_pref = runtime.get("device_preference", "cpu")  # :contentReference[oaicite:3]{index=3}
            if device_pref == "cuda" and torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"

        # Sequence config :contentReference[oaicite:4]{index=4}
        seq = cfg.get("sequence", {})
        max_len = int(seq.get("max_len", settings.MAX_LEN))
        unk_token = str(seq.get("unk_token", "<UNK>"))

        # Decode config :contentReference[oaicite:5]{index=5}
        dec = cfg.get("decode", {})
        decode_insert_label = int(dec.get("insert_space_on_label", 1))
        preserve_existing_spaces = bool(dec.get("preserve_existing_spaces", False))

        # Load vocab
        vocab = load_vocab(vocab_path)
        vocab_size = len(vocab)

        # Model config :contentReference[oaicite:6]{index=6}
        m = cfg.get("model", {})
        model = KhmerRNN(
            vocab_size=vocab_size,
            embedding_dim=int(m.get("embedding_dim", 128)),
            hidden_dim=int(m.get("hidden_dim", 256)),
            num_layers=int(m.get("num_layers", 2)),
            dropout=float(m.get("dropout", 0.2)),
            bidirectional=bool(m.get("bidirectional", True)),
            rnn_type=str(m.get("arch", "lstm")),
            residual=False,
            use_crf=False,
        )

        state = torch.load(str(ckpt_path), map_location=device)
        model.load_state_dict(state)
        model.to(device)
        model.eval()

        return cls(
            model=model,
            vocab=vocab,
            device=device,
            max_len=max_len,
            unk_token=unk_token,
            decode_insert_label=decode_insert_label,
            preserve_existing_spaces=preserve_existing_spaces,
        )

    @torch.no_grad()
    def segment(self, text: str) -> str:
        text = _preprocess(text, _load_config(settings.artifact_path / "config.json"))
        if not text:
            return ""

        if len(text) > settings.MAX_TEXT_CHARS:
            raise ValueError(f"Text too large: {len(text)} chars (limit {settings.MAX_TEXT_CHARS})")

        # If you want to preserve existing spaces, segment each “word-run” separately
        if self.preserve_existing_spaces:
            parts = text.split(" ")
            seg_parts = [self._segment_no_spaces(p) for p in parts]
            return " ".join(seg_parts)

        # Otherwise, remove spaces before running segmentation (common for “space injector”)
        text_no_spaces = text.replace(" ", "")
        return self._segment_no_spaces(text_no_spaces)

    def _segment_no_spaces(self, text: str) -> str:
        if not text:
            return ""

        unk_id = self.vocab.get(self.unk_token, self.vocab.get("<UNK>", 1))
        outputs: List[str] = []

        for ch in chunk_text(text, self.max_len):
            ids = [self.vocab.get(c, unk_id) for c in ch]
            x = torch.tensor(ids, dtype=torch.long).unsqueeze(0).to(self.device)

            logits = self.model(x)  # (1, T, 2)
            pred = logits.argmax(dim=-1).squeeze(0).tolist()

            outputs.append(
                decode_spaces(
                    ch,
                    pred,
                    insert_on_label=self.decode_insert_label,
                )
            )

        return "".join(outputs)
