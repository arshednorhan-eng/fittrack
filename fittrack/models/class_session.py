from datetime import datetime
from fittrack.database import db

class ClassSession(db.Model):
    __tablename__ = "class_sessions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    starts_at = db.Column(db.DateTime, nullable=False, index=True)
    capacity = db.Column(db.Integer, nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="scheduled")  # scheduled/canceled/closed

    trainer = db.relationship("Trainer", back_populates="class_sessions")
    enrollments = db.relationship("Enrollment", back_populates="class_session", cascade="all, delete-orphan")
