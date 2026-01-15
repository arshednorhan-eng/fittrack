from datetime import datetime
from fittrack.database import db

class WorkoutPlan(db.Model):
    __tablename__ = "workout_plans"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False, index=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.id"), nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    member = db.relationship("Member", back_populates="workout_plans")
    trainer = db.relationship("Trainer", back_populates="workout_plans")
    items = db.relationship("WorkoutItem", back_populates="plan", cascade="all, delete-orphan")
