from datetime import date, timedelta

from fittrack.database import db
from fittrack.models.subscription import Subscription
from fittrack.models.member import Member
from fittrack.models.plan import Plan
from fittrack.models.payment import Payment
from fittrack.exceptions import NotFoundError, BusinessRuleError


def assign_subscription(schema):
    member = db.session.get(Member, schema.member_id)
    if not member:
        raise NotFoundError("Member not found")

    plan = db.session.get(Plan, schema.plan_id)
    if not plan:
        raise NotFoundError("Plan not found")

    start = schema.start_date or date.today()
    end = start + timedelta(days=plan.valid_days) if plan.valid_days else None

    remaining = plan.max_entries if plan.type == "card" else None

    sub = Subscription(
        member_id=member.id,
        plan_id=plan.id,
        status="active",
        start_date=start,
        end_date=end,
        remaining_entries=remaining,
    )
    db.session.add(sub)

    # default payment
    pay = Payment(subscription=sub, amount=plan.price, status="paid", reference="seed")
    db.session.add(pay)

    db.session.commit()
    return sub


def freeze_subscription(schema):
    sub = _get_active_subscription_for_member(schema.member_id)
    sub.status = "frozen"
    sub.frozen_until = schema.until
    db.session.commit()
    return sub


def subscription_status(member_id: int):
    sub = _get_latest_subscription_for_member(member_id)
    status = compute_subscription_state(sub)
    return sub, status


def _get_latest_subscription_for_member(member_id: int) -> Subscription:
    sub = (
        Subscription.query
        .filter_by(member_id=member_id)
        .order_by(Subscription.id.desc())
        .first()
    )
    if not sub:
        raise NotFoundError("Subscription not found for member")
    return sub


def _get_active_subscription_for_member(member_id: int) -> Subscription:
    sub = (
        Subscription.query
        .filter_by(member_id=member_id, status="active")
        .order_by(Subscription.id.desc())
        .first()
    )
    if not sub:
        raise NotFoundError("Active subscription not found for member")
    return sub


def compute_subscription_state(sub: Subscription) -> str:
    today = date.today()

    # debt rule: any pending payment blocks
    has_pending = any(p.status == "pending" for p in sub.payments)
    if has_pending:
        return "debt"

    if sub.status == "frozen":
        if sub.frozen_until and sub.frozen_until < today:
            # auto-unfreeze
            sub.status = "active"
            sub.frozen_until = None
            db.session.commit()
        else:
            return "frozen"

    if sub.end_date and sub.end_date < today:
        return "expired"

    if sub.plan.type == "card":
        if sub.remaining_entries is not None and sub.remaining_entries <= 0:
            return "expired"

    return "active"


def consume_entry_if_needed(sub: Subscription):
    if sub.plan.type != "card":
        return

    if sub.remaining_entries is None:
        raise BusinessRuleError("Card subscription missing remaining entries")
    if sub.remaining_entries <= 0:
        raise BusinessRuleError("No remaining entries")

    sub.remaining_entries -= 1
    db.session.commit()
