from datetime import datetime
from fittrack.database import db
from fittrack.models.class_session import ClassSession
from fittrack.models.enrollment import Enrollment
from fittrack.models.member import Member
from fittrack.models.trainer import Trainer
from fittrack.exceptions import NotFoundError, BusinessRuleError, DuplicateError


def create_class(schema):
    trainer = db.session.get(Trainer, schema.trainer_id)
    if not trainer:
        raise NotFoundError("Trainer not found")

    cs = ClassSession(
        title=schema.title,
        starts_at=schema.starts_at,
        capacity=schema.capacity,
        trainer_id=trainer.id,
        status="scheduled",
    )
    db.session.add(cs)
    db.session.commit()
    return cs


def enroll(schema):
    cs = db.session.get(ClassSession, schema.class_session_id)
    if not cs:
        raise NotFoundError("Class session not found")

    member = db.session.get(Member, schema.member_id)
    if not member:
        raise NotFoundError("Member not found")

    if cs.status != "scheduled":
        raise BusinessRuleError("Class session is not open for enrollment")

    existing = Enrollment.query.filter_by(class_session_id=cs.id, member_id=member.id).first()
    if existing and existing.status != "canceled":
        raise DuplicateError("Member already enrolled/waiting in this class")

    enrolled_count = Enrollment.query.filter_by(class_session_id=cs.id, status="enrolled").count()
    new_status = "enrolled" if enrolled_count < cs.capacity else "waiting"

    if existing and existing.status == "canceled":
        existing.status = new_status
        existing.canceled_at = None
        existing.cancel_reason = None
        db.session.commit()
        return existing

    e = Enrollment(class_session_id=cs.id, member_id=member.id, status=new_status)
    db.session.add(e)
    db.session.commit()
    return e


def cancel(schema):
    e = Enrollment.query.filter_by(
        class_session_id=schema.class_session_id,
        member_id=schema.member_id
    ).first()

    if not e or e.status == "canceled":
        raise NotFoundError("Enrollment not found")

    e.status = "canceled"
    e.canceled_at = datetime.utcnow()
    e.cancel_reason = schema.reason
    db.session.commit()

    _promote_waiting_if_possible(e.class_session_id)
    return e


def list_participants(class_session_id: int):
    cs = db.session.get(ClassSession, class_session_id)
    if not cs:
        raise NotFoundError("Class session not found")

    enrollments = (
        Enrollment.query
        .filter_by(class_session_id=class_session_id)
        .order_by(Enrollment.created_at.asc())
        .all()
    )
    return cs, enrollments


def _promote_waiting_if_possible(class_session_id: int):
    cs = db.session.get(ClassSession, class_session_id)
    if not cs:
        return

    enrolled_count = Enrollment.query.filter_by(class_session_id=cs.id, status="enrolled").count()
    if enrolled_count >= cs.capacity:
        return

    next_waiting = (
        Enrollment.query
        .filter_by(class_session_id=cs.id, status="waiting")
        .order_by(Enrollment.created_at.asc())
        .first()
    )
    if next_waiting:
        next_waiting.status = "enrolled"
        db.session.commit()
