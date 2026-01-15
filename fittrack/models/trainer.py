from fittrack.database import db

_ALLOWED_STATUSES = {"active", "inactive"}

class Trainer(db.Model):
    __tablename__ = "trainers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    _status = db.Column("status", db.String(20), nullable=False, default="active")

    class_sessions = db.relationship("ClassSession", back_populates="trainer")
    workout_plans = db.relationship("WorkoutPlan", back_populates="trainer")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        v = (value or "").lower().strip()
        if v not in _ALLOWED_STATUSES:
            raise ValueError("Invalid trainer status")
        self._status = v
