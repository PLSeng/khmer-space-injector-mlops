from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.record import SegmentRecord

class RecordRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, input_text: str, output_text: str) -> SegmentRecord:
        rec = SegmentRecord(input_text=input_text, output_text=output_text)
        self.db.add(rec)
        await self.db.commit()
        await self.db.refresh(rec)
        return rec

    async def list(self, limit: int = 50, offset: int = 0):
        q = select(SegmentRecord).order_by(desc(SegmentRecord.created_at)).limit(limit).offset(offset)
        res = await self.db.execute(q)
        return list(res.scalars().all())
