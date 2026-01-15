from datetime import datetime
from fittrack.database import db

class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    class_session_id = db.Column(db.Integer, db.ForeignKey("class_sessions.id"), nullable=False, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False, index=True)

    status = db.Column(db.String(20), nullable=False, default="enrolled")  # enrolled/waiting/canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canceled_at = db.Column(db.DateTime, nullable=True)
    cancel_reason = db.Column(db.String(200), nullable=True)

    class_session = db.relationship("ClassSession", back_populates="enrollments")
    member = db.relationship("Member", back_populates="enrollments")

    __table_args__ = (
        db.UniqueConstraint("class_session_id", "member_id", name="uq_enrollment_class_member"),
    )
