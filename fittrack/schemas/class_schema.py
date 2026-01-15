from datetime import datetime
from pydantic import BaseModel, Field

class CreateClassSession(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    starts_at: datetime
    capacity: int = Field(gt=0, le=500)
    trainer_id: int = Field(gt=0)

class EnrollToClass(BaseModel):
    class_session_id: int = Field(gt=0)
    member_id: int = Field(gt=0)

class CancelEnrollment(BaseModel):
    class_session_id: int = Field(gt=0)
    member_id: int = Field(gt=0)
    reason: str | None = Field(default=None, max_length=200)
