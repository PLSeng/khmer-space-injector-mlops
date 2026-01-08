from pydantic import BaseModel

class RecordOut(BaseModel):
    id: str
    input_text: str
    output_text: str
    created_at: str
