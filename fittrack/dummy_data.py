"""
Seed / reset database with dummy data.

Run:
    python dummy_data.py
"""

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from fittrack.app import create_app
from fittrack.database import db
from fittrack.models import Member, Trainer, Plan, ClassSession


def seed():
    app = create_app()
    with app.app_context():
        # Reset DB
        db.drop_all()
        db.create_all()

        # ======================
        # Trainers
        # ======================
        t1 = Trainer(
            full_name="Dana Trainer",
            email="trainer1@mail.com",
            phone="0501111111",
            status="active"
        )

        t2 = Trainer(
            full_name="Omer Trainer",
            email="trainer2@mail.com",
            phone="0502222222",
            status="active"
        )

        # ======================
        # Members
        # ======================
        m1 = Member(
            full_name="Noa Member",
            email="noa@mail.com",
            phone="0501234567",
            national_id="123456789",
            password_hash=generate_password_hash("Aa1@aaaa"),
        )
        m1.status = "active"

        m2 = Member(
            full_name="Lior Member",
            email="lior@mail.com",
            phone="0507654321",
            national_id="234567890",
            password_hash=generate_password_hash("Aa1@bbbb"),
        )
        m2.status = "active"

        m3 = Member(
            full_name="Maya Member",
            email="maya@mail.com",
            phone="0503333333",
            national_id="345678901",
            password_hash=generate_password_hash("Aa1@cccc"),
        )
        m3.status = "active"

        # ======================
        # Plans
        # ======================
        p_monthly = Plan(
            name="Monthly Unlimited",
            type="monthly",
            price=250.0,
            valid_days=30,
            max_entries=None
        )

        p_card10 = Plan(
            name="Card 10 Entries",
            type="card",
            price=180.0,
            valid_days=90,
            max_entries=10
        )

        # ======================
        # Commit base data
        # ======================
        db.session.add_all([
            t1, t2,
            m1, m2, m3,
            p_monthly, p_card10
        ])
        db.session.commit()

        # ======================
        # Classes
        # ======================
        cs1 = ClassSession(
            title="Yoga",
            starts_at=datetime.utcnow() + timedelta(days=1),
            capacity=2,
            trainer_id=t1.id,
            status="scheduled"
        )

        cs2 = ClassSession(
            title="Pilates",
            starts_at=datetime.utcnow() + timedelta(days=2),
            capacity=3,
            trainer_id=t2.id,
            status="scheduled"
        )

        db.session.add_all([cs1, cs2])
        db.session.commit()

        # ======================
        # Output
        # ======================
        print("✅ Database seeded successfully.")
        print("Members:", [m1.id, m2.id, m3.id])
        print("Trainers:", [t1.id, t2.id])
        print("Plans:", [p_monthly.id, p_card10.id])
        print("Classes:", [cs1.id, cs2.id])


if __name__ == "__main__":
    seed()
