from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.segment import SegmentRequest, SegmentResponse
from app.db.session import get_db
from app.db.repo.record_repo import RecordRepo
from app.main_state import get_segmenter

router = APIRouter(prefix="/api", tags=["segment"])

@router.post("/segment", response_model=SegmentResponse)
async def segment(payload: SegmentRequest, db: AsyncSession = Depends(get_db)):
    seg = get_segmenter()
    try:
        output = seg.segment(payload.text)
    except ValueError as e:
        raise HTTPException(status_code=413, detail=str(e))

    rec = await RecordRepo(db).create(input_text=payload.text, output_text=output)

    return SegmentResponse(
        output=output,
        record_id=str(rec.id),
        created_at=rec.created_at.isoformat(),
    )
