from datetime import date
from fittrack.database import db

class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False, index=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.id"), nullable=False, index=True)

    status = db.Column(db.String(20), nullable=False, default="active")  # active/frozen/expired/debt
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date, nullable=True)

    remaining_entries = db.Column(db.Integer, nullable=True)  # card type only; monthly can be None
    frozen_until = db.Column(db.Date, nullable=True)

    member = db.relationship("Member", back_populates="subscriptions")
    plan = db.relationship("Plan", back_populates="subscriptions")
    payments = db.relationship("Payment", back_populates="subscription", cascade="all, delete-orphan")
