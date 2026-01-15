from werkzeug.security import generate_password_hash
from fittrack.database import db
from fittrack.models.member import Member
from fittrack.exceptions import NotFoundError, DuplicateError


def create_member(schema):
    if Member.query.filter_by(email=str(schema.email)).first():
        raise DuplicateError("Member with this email already exists")

    if Member.query.filter_by(national_id=schema.national_id).first():
        raise DuplicateError("Member with this national_id already exists")

    m = Member(
        full_name=schema.full_name,
        email=str(schema.email),
        phone=schema.phone,
        national_id=schema.national_id,
        password_hash=generate_password_hash(schema.password),
    )
    db.session.add(m)
    db.session.commit()
    return m


def get_member(member_id: int) -> Member:
    m = db.session.get(Member, member_id)
    if not m:
        raise NotFoundError("Member not found")
    return m


def update_member(member_id: int, schema):
    m = get_member(member_id)
    if schema.full_name is not None:
        m.full_name = schema.full_name
    if schema.phone is not None:
        m.phone = schema.phone
    if schema.status is not None:
        m.status = schema.status  # setter validates
    db.session.commit()
    return m
