from flask import Blueprint, jsonify
from pydantic import ValidationError

from fittrack.routes._helpers import parse_json, validation_error_to_response, require_roles
from fittrack.schemas.subscription_schema import AssignSubscription, FreezeSubscription
from fittrack.services import subscription_service

bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")


@bp.post("/assign")
@require_roles("admin")
def assign():
    try:
        schema = parse_json(AssignSubscription)
    except ValidationError as e:
        return validation_error_to_response(e)

    sub = subscription_service.assign_subscription(schema)
    return jsonify(_sub_to_dict(sub)), 201


@bp.put("/freeze")
@require_roles("admin", "trainer")
def freeze():
    try:
        schema = parse_json(FreezeSubscription)
    except ValidationError as e:
        return validation_error_to_response(e)

    sub = subscription_service.freeze_subscription(schema)
    return jsonify(_sub_to_dict(sub)), 200


@bp.get("/status/<int:member_id>")
@require_roles("admin", "trainer", "member")
def status(member_id: int):
    sub, computed = subscription_service.subscription_status(member_id)
    data = _sub_to_dict(sub)
    data["computed_status"] = computed
    return jsonify(data), 200


def _sub_to_dict(sub):
    return {
        "id": sub.id,
        "member_id": sub.member_id,
        "plan_id": sub.plan_id,
        "status": sub.status,
        "start_date": sub.start_date.isoformat() if sub.start_date else None,
        "end_date": sub.end_date.isoformat() if sub.end_date else None,
        "remaining_entries": sub.remaining_entries,
        "frozen_until": sub.frozen_until.isoformat() if sub.frozen_until else None,
    }
