from datetime import datetime
from fittrack.database import db

class CheckIn(db.Model):
    __tablename__ = "checkins"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    result = db.Column(db.String(20), nullable=False)  # approved/denied
    reason = db.Column(db.String(200), nullable=True)

    member = db.relationship("Member", back_populates="checkins")
