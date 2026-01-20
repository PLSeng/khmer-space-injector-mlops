from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.record import Record

router = APIRouter()

@router.get("/api/history")
def history(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Record)
        .order_by(Record.id.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": r.id,
            "input_text": r.input_text,
            "output_text": r.output_text,
            "created_at": r.created_at,
        }
        for r in rows
    ]
