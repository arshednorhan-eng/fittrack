from datetime import datetime
from fittrack.database import db

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False, index=True)

    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="paid")  # paid/pending/canceled/refunded
    paid_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    reference = db.Column(db.String(120), nullable=True)

    subscription = db.relationship("Subscription", back_populates="payments")
