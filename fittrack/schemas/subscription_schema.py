from pydantic import BaseModel, Field
from datetime import date

class AssignSubscription(BaseModel):
    member_id: int
    plan_id: int
    start_date: date | None = None  # optional

class FreezeSubscription(BaseModel):
    member_id: int
    until: date
