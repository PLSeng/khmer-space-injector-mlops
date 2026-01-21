from sqlalchemy.orm import Session
from app.models.record import Record

def save_record(db: Session, input_text: str, output_text: str) -> Record:
    rec = Record(input_text=input_text, output_text=output_text)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
