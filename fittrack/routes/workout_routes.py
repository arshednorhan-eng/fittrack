from flask import Blueprint, jsonify
from pydantic import ValidationError

from fittrack.routes._helpers import parse_json, validation_error_to_response, require_roles
from fittrack.schemas.workout_schema import WorkoutPlanCreate
from fittrack.services import workout_service

bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@bp.post("/")
@require_roles("trainer", "admin")
def create_workout():
    try:
        schema = parse_json(WorkoutPlanCreate)
    except ValidationError as e:
        return validation_error_to_response(e)

    plan = workout_service.create_workout_plan(schema)
    return jsonify(_plan_to_dict(plan)), 201


@bp.get("/<int:member_id>")
@require_roles("trainer", "admin", "member")
def get_member_plans(member_id: int):
    plans = workout_service.get_workout_plans_for_member(member_id)
    return jsonify([_plan_to_dict(p) for p in plans]), 200


def _plan_to_dict(p):
    return {
        "id": p.id,
        "member_id": p.member_id,
        "trainer_id": p.trainer_id,
        "title": p.title,
        "created_at": p.created_at.isoformat(),
        "is_active": p.is_active,
        "items": [
            {
                "id": i.id,
                "exercise_name": i.exercise_name,
                "sets": i.sets,
                "reps": i.reps,
                "target_weight": i.target_weight,
                "notes": i.notes
            }
            for i in p.items
        ]
    }
