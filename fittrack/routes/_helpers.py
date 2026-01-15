from functools import wraps
from flask import request
from pydantic import ValidationError

def parse_json(model_cls):
    """Parse and validate request JSON with Pydantic. Raises ValidationError."""
    payload = request.get_json(silent=True)
    if payload is None:
        payload = {}
    return model_cls.model_validate(payload)

def validation_error_to_response(e: ValidationError):
    return {
        "error": "ValidationError",
        "details": e.errors(),
    }, 422

def require_roles(*allowed_roles: str):
    """
    Basic authorization:
    Client must send header: X-ROLE: admin / trainer / member
    """
    allowed = {r.lower() for r in allowed_roles}

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = (request.headers.get("X-ROLE") or "").lower().strip()
            if role not in allowed:
                return {
                    "error": "Forbidden",
                    "message": f"Role '{role or 'missing'}' is not allowed for this endpoint",
                    "allowed_roles": sorted(list(allowed)),
                }, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def serialize(schema_cls, obj):
    """
    Convert SQLAlchemy model (or plain dict) -> Pydantic Response schema -> dict
    """
    if obj is None:
        return None
    if isinstance(obj, dict):
        return schema_cls.model_validate(obj).model_dump()
    return schema_cls.model_validate(obj, from_attributes=True).model_dump()
