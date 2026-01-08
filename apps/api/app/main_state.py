from typing import Optional
from app.services.segmenter import Segmenter

_segmenter: Optional[Segmenter] = None

def set_segmenter(seg: Segmenter) -> None:
    global _segmenter
    _segmenter = seg

def get_segmenter() -> Segmenter:
    if _segmenter is None:
        raise RuntimeError("Segmenter not initialized")
    return _segmenter
