from pydantic import BaseModel

class CheckInRequest(BaseModel):
    member_id: int
