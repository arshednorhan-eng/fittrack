from flask import Blueprint, jsonify
from pydantic import ValidationError

from fittrack.routes._helpers import parse_json, validation_error_to_response, require_roles
from fittrack.schemas.class_schema import CreateClassSession, EnrollToClass, CancelEnrollment
from fittrack.services import class_service

bp = Blueprint("classes", __name__, url_prefix="/classes")


@bp.post("/")
@require_roles("admin", "trainer")
def create_class():
    try:
        schema = parse_json(CreateClassSession)
    except ValidationError as e:
        return validation_error_to_response(e)

    cs = class_service.create_class(schema)
    return jsonify(_class_to_dict(cs)), 201


@bp.post("/enroll")
@require_roles("member", "admin")
def enroll():
    try:
        schema = parse_json(EnrollToClass)
    except ValidationError as e:
        return validation_error_to_response(e)

    e = class_service.enroll(schema)
    return jsonify(_enrollment_to_dict(e)), 201


@bp.delete("/cancel")
@require_roles("member", "admin")
def cancel():
    try:
        schema = parse_json(CancelEnrollment)
    except ValidationError as e:
        return validation_error_to_response(e)

    e = class_service.cancel(schema)
    return jsonify(_enrollment_to_dict(e)), 200


@bp.get("/<int:class_id>/participants")
@require_roles("admin", "trainer")
def participants(class_id: int):
    cs, enrollments = class_service.list_participants(class_id)
    return jsonify({
        "class": _class_to_dict(cs),
        "participants": [
            {
                "enrollment_id": e.id,
                "member_id": e.member_id,
                "status": e.status,
                "created_at": e.created_at.isoformat(),
                "canceled_at": e.canceled_at.isoformat() if e.canceled_at else None,
                "cancel_reason": e.cancel_reason
            } for e in enrollments
        ]
    }), 200


def _class_to_dict(cs):
    return {
        "id": cs.id,
        "title": cs.title,
        "starts_at": cs.starts_at.isoformat(),
        "capacity": cs.capacity,
        "trainer_id": cs.trainer_id,
        "status": cs.status
    }


def _enrollment_to_dict(e):
    return {
        "id": e.id,
        "class_session_id": e.class_session_id,
        "member_id": e.member_id,
        "status": e.status,
        "created_at": e.created_at.isoformat(),
        "canceled_at": e.canceled_at.isoformat() if e.canceled_at else None,
        "cancel_reason": e.cancel_reason
    }
