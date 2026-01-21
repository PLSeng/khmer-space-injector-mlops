from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.repo.record_repo import list_records

router = APIRouter()

@router.get("/api/records")
def records(limit: int = 50, db: Session = Depends(get_db)):
    rows = list_records(db, limit=limit)
    return [
        {
            "id": r.id,
            "input_text": r.input_text,
            "output_text": r.output_text,
            "created_at": r.created_at,
        }
        for r in rows
    ]