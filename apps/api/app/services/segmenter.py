from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

import torch

from app.core.config import settings
from app.services.artifacts import load_vocab
from app.services.utils import chunk_text
from app.services.utils import decode_spaces  # you can move your decode here
from app.services.net import KhmerRNN          # copy your model class here


@dataclass
class Segmenter:
    model: KhmerRNN
    vocab: Dict[str, int]
    device: str

    @classmethod
    def load_from_artifacts(cls, artifact_dir: Path, device: str) -> "Segmenter":
        vocab_path = artifact_dir / "vocab.json"
        ckpt_path = artifact_dir / "checkpoint.pt"

        vocab = load_vocab(vocab_path)
        vocab_size = len(vocab)

        model = KhmerRNN(
            vocab_size=vocab_size,
            embedding_dim=128,
            hidden_dim=256,
            num_layers=2,
            dropout=0.3,
            bidirectional=True,
            rnn_type="lstm",
            residual=False,
            use_crf=False,
        )

        state = torch.load(str(ckpt_path), map_location=device)
        model.load_state_dict(state)
        model.to(device)
        model.eval()

        return cls(model=model, vocab=vocab, device=device)

    @torch.no_grad()
    def segment(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return ""

        if len(text) > settings.MAX_TEXT_CHARS:
            raise ValueError(f"Text too large: {len(text)} chars (limit {settings.MAX_TEXT_CHARS})")

        unk = self.vocab.get("<UNK>", 1)
        outputs: List[str] = []

        for ch in chunk_text(text, settings.MAX_LEN):
            ids = [self.vocab.get(c, unk) for c in ch]
            x = torch.tensor(ids, dtype=torch.long).unsqueeze(0).to(self.device)

            logits = self.model(x)  # (1, T, 2)
            pred = logits.argmax(dim=-1).squeeze(0).tolist()
            outputs.append(decode_spaces(ch, pred))

        return "".join(outputs)
