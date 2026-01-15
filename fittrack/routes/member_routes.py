from flask import Blueprint, jsonify
from pydantic import ValidationError

from fittrack.routes._helpers import parse_json, validation_error_to_response, require_roles, serialize
from fittrack.schemas.member_schema import MemberCreate, MemberUpdate, MemberResponse
from fittrack.services import member_service

bp = Blueprint("members", __name__, url_prefix="/members")


@bp.post("/")
@require_roles("admin")
def create_member():
    try:
        schema = parse_json(MemberCreate)
    except ValidationError as e:
        return validation_error_to_response(e)

    m = member_service.create_member(schema)

    data = serialize(MemberResponse, {
        "id": m.id,
        "full_name": m.full_name,
        "email": m.email,
        "phone": m.phone,
        "national_id": m.national_id,
        "status": m.status,
        "created_at": m.created_at.isoformat(),
    })
    return jsonify(data), 201


@bp.get("/<int:member_id>")
@require_roles("admin", "trainer", "member")
def get_member(member_id: int):
    m = member_service.get_member(member_id)
    return jsonify(serialize(MemberResponse, {
        "id": m.id,
        "full_name": m.full_name,
        "email": m.email,
        "phone": m.phone,
        "national_id": m.national_id,
        "status": m.status,
        "created_at": m.created_at.isoformat(),
    })), 200


@bp.put("/<int:member_id>")
@require_roles("admin", "trainer")
def update_member(member_id: int):
    try:
        schema = parse_json(MemberUpdate)
    except ValidationError as e:
        return validation_error_to_response(e)

    m = member_service.update_member(member_id, schema)
    return jsonify(serialize(MemberResponse, {
        "id": m.id,
        "full_name": m.full_name,
        "email": m.email,
        "phone": m.phone,
        "national_id": m.national_id,
        "status": m.status,
        "created_at": m.created_at.isoformat(),
    })), 200
