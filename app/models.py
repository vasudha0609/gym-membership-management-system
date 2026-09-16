from datetime import datetime, date
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """App login accounts (admin/staff). Not part of the gym data schema itself."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="staff")  # admin, staff
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Trainer(db.Model):
    __tablename__ = "trainers"

    trainer_id = db.Column(db.Integer, primary_key=True)
    trainer_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    phone = db.Column(db.String(15))

    members = db.relationship("Member", backref="trainer", lazy=True)


class Plan(db.Model):
    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # days
    price = db.Column(db.Numeric(10, 2), nullable=False)

    memberships = db.relationship("Membership", backref="plan", lazy=True)


class Member(db.Model):
    __tablename__ = "members"

    member_id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15))
    join_date = db.Column(db.Date, default=date.today)

    # Extension beyond the base schema: lets a trainer be assigned to a member.
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.trainer_id"))

    memberships = db.relationship("Membership", backref="member", lazy=True,
                                   cascade="all, delete-orphan")
    payments = db.relationship("Payment", backref="member", lazy=True,
                                cascade="all, delete-orphan")

    @property
    def current_membership(self):
        active = [m for m in self.memberships if m.end_date and m.end_date >= date.today()]
        if active:
            return max(active, key=lambda m: m.end_date)
        if self.memberships:
            return max(self.memberships, key=lambda m: m.end_date)
        return None

    @property
    def membership_status(self):
        m = self.current_membership
        if not m:
            return "No Plan"
        return "Active" if m.end_date >= date.today() else "Expired"

    @property
    def total_spent(self):
        return sum((p.amount for p in self.payments if p.status == "Completed"), 0)


class Membership(db.Model):
    __tablename__ = "memberships"

    membership_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.member_id"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.plan_id"), nullable=False)
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date, nullable=False)


class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.member_id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default="Completed")  # Completed, Pending, Failed
