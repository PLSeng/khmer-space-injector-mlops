from pydantic import BaseModel, Field

class SegmentRequest(BaseModel):
    text: str = Field(..., min_length=1)

class SegmentResponse(BaseModel):
    output: str
    record_id: str
    created_at: str