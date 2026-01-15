from flask import Blueprint, jsonify
from pydantic import ValidationError

from fittrack.routes._helpers import parse_json, validation_error_to_response, require_roles
from fittrack.schemas.checkin_schema import CheckInRequest
from fittrack.services import checkin_service

bp = Blueprint("checkin", __name__, url_prefix="/checkin")


@bp.post("/")
@require_roles("member", "admin")
def do_checkin():
    try:
        schema = parse_json(CheckInRequest)
    except ValidationError as e:
        return validation_error_to_response(e)

    ci = checkin_service.check_in(schema.member_id)
    return jsonify({
        "id": ci.id,
        "member_id": ci.member_id,
        "created_at": ci.created_at.isoformat(),
        "result": ci.result,
        "reason": ci.reason
    }), 201
