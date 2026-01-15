from fittrack.database import db
from fittrack.models.checkin import CheckIn
from fittrack.models.member import Member
from fittrack.exceptions import NotFoundError
from fittrack.services.subscription_service import (
    _get_latest_subscription_for_member,
    compute_subscription_state,
    consume_entry_if_needed,
)

def check_in(member_id: int):
    member = db.session.get(Member, member_id)
    if not member:
        raise NotFoundError("Member not found")

    sub = _get_latest_subscription_for_member(member_id)
    state = compute_subscription_state(sub)

    if member.status in ("blocked", "pending"):
        ci = CheckIn(member_id=member_id, result="denied", reason=f"Member status: {member.status}")
        db.session.add(ci)
        db.session.commit()
        return ci

    if state != "active":
        ci = CheckIn(member_id=member_id, result="denied", reason=f"Subscription status: {state}")
        db.session.add(ci)
        db.session.commit()
        return ci

    # consume entry for card plans (function can decide if needed)
    if sub.plan.type == "card":
        consume_entry_if_needed(sub)

    ci = CheckIn(member_id=member_id, result="approved", reason=None)
    db.session.add(ci)
    db.session.commit()
    return ci
