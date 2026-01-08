from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.repo.record_repo import RecordRepo
from app.schemas.record import RecordOut

router = APIRouter(prefix="/api", tags=["records"])

@router.get("/records", response_model=list[RecordOut])
async def records(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    rows = await RecordRepo(db).list(limit=limit, offset=offset)
    return [
        RecordOut(
            id=str(r.id),
            input_text=r.input_text,
            output_text=r.output_text,
            created_at=r.created_at.isoformat(),
        )
        for r in rows
    ]
