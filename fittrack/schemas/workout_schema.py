from pydantic import BaseModel, Field
from typing import List

class WorkoutItemCreate(BaseModel):
    exercise_name: str = Field(min_length=2, max_length=120)
    sets: int = Field(gt=0, le=50)
    reps: int = Field(gt=0, le=200)
    target_weight: float | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=200)

class WorkoutPlanCreate(BaseModel):
    member_id: int
    trainer_id: int
    title: str = Field(min_length=2, max_length=120)
    items: List[WorkoutItemCreate] = Field(min_length=1)
