from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.core.config import settings
from app.core.metrics import metrics, Timer
from app.api.deps import get_db
from app.db.repo.record_repo import save_record
from app.schemas.segment import SegmentRequest, SegmentResponse
from app.services.segmenter import Segmenter

logger = logging.getLogger(__name__)
router = APIRouter()

_segmenter = Segmenter.load_from_artifacts(settings.artifact_path, device=None)

@router.post("/api/segment", response_model=SegmentResponse)
def segment(req: SegmentRequest, db: Session = Depends(get_db)):
    metrics.inc_requests()

    try:
        with Timer() as t:
            output = _segmenter.segment(req.text)
        metrics.observe_segment_latency(t.elapsed_ms)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if settings.ENABLE_DB_LOGGING:
        try:
            save_record(db, input_text=req.text, output_text=output)
        except Exception as e:
            logger.warning("DB logging failed: %s", e)

    return SegmentResponse(input=req.text, output=output)
