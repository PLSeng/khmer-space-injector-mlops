from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    input_text: str
    output_text: str
    created_at: datetime