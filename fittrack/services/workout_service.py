from fittrack.database import db
from fittrack.models.workout_plan import WorkoutPlan
from fittrack.models.workout_item import WorkoutItem
from fittrack.models.member import Member
from fittrack.models.trainer import Trainer
from fittrack.exceptions import NotFoundError


def create_workout_plan(schema):
    member = db.session.get(Member, schema.member_id)
    if not member:
        raise NotFoundError("Member not found")

    trainer = db.session.get(Trainer, schema.trainer_id)
    if not trainer:
        raise NotFoundError("Trainer not found")

    plan = WorkoutPlan(member_id=member.id, trainer_id=trainer.id, title=schema.title, is_active=True)
    db.session.add(plan)
    db.session.flush()  # get id before adding items

    for item in schema.items:
        wi = WorkoutItem(
            plan_id=plan.id,
            exercise_name=item.exercise_name,
            sets=item.sets,
            reps=item.reps,
            target_weight=item.target_weight,
            notes=item.notes,
        )
        db.session.add(wi)

    db.session.commit()
    return plan


def get_workout_plans_for_member(member_id: int):
    plans = (
        WorkoutPlan.query
        .filter_by(member_id=member_id)
        .order_by(WorkoutPlan.created_at.desc())
        .all()
    )
    if not plans:
        raise NotFoundError("No workout plans found for member")
    return plans
