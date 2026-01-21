from pydantic import BaseModel, Field, ConfigDict

class SegmentRequest(BaseModel):
    text: str = Field(..., min_length=1)

class SegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    input: str
    output: str