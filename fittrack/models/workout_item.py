from fittrack.database import db

class WorkoutItem(db.Model):
    __tablename__ = "workout_items"

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("workout_plans.id"), nullable=False, index=True)

    exercise_name = db.Column(db.String(120), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    target_weight = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(200), nullable=True)

    plan = db.relationship("WorkoutPlan", back_populates="items")
