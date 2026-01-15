from datetime import datetime
from fittrack.database import db

_ALLOWED_STATUSES = {"active", "frozen", "blocked", "pending"}

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)

    national_id = db.Column(db.String(9), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    _status = db.Column("status", db.String(20), nullable=False, default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    subscriptions = db.relationship("Subscription", back_populates="member", cascade="all, delete-orphan")
    enrollments = db.relationship("Enrollment", back_populates="member", cascade="all, delete-orphan")
    workout_plans = db.relationship("WorkoutPlan", back_populates="member", cascade="all, delete-orphan")
    checkins = db.relationship("CheckIn", back_populates="member", cascade="all, delete-orphan")

    # Encapsulation: getter/setter for status
    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        v = (value or "").strip().lower()
        if v not in _ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{value}'. Allowed: {sorted(_ALLOWED_STATUSES)}")
        self._status = v
