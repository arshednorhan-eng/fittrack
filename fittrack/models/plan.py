from fittrack.database import db

class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # monthly/card/pt_package
    price = db.Column(db.Float, nullable=False)
    valid_days = db.Column(db.Integer, nullable=True)  # e.g., 30 for monthly, 90 for card, etc.
    max_entries = db.Column(db.Integer, nullable=True)  # card visits. monthly can be None/unlimited

    subscriptions = db.relationship("Subscription", back_populates="plan")
