from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from app import db
from app.models import Member, Plan, Membership, Payment, Trainer

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/")
@login_required
def index():
    # Top 5 most popular plans (by number of memberships)
    top_plans = db.session.query(
        Plan.plan_name, func.count(Membership.membership_id).label("signups")
    ).join(Membership, Membership.plan_id == Plan.plan_id) \
        .group_by(Plan.plan_id, Plan.plan_name) \
        .order_by(func.count(Membership.membership_id).desc()) \
        .limit(5).all()

    # Most active members (by number of completed payments)
    most_active = db.session.query(
        Member.member_name, func.count(Payment.payment_id).label("payment_count")
    ).join(Payment, Payment.member_id == Member.member_id) \
        .filter(Payment.status == "Completed") \
        .group_by(Member.member_id, Member.member_name) \
        .order_by(func.count(Payment.payment_id).desc()) \
        .limit(10).all()

    # Monthly revenue report
    month_expr = func.strftime("%Y-%m", Payment.payment_date) \
        if db.engine.name == "sqlite" else func.to_char(Payment.payment_date, "YYYY-MM")
    monthly_revenue = db.session.query(
        month_expr.label("month"), func.sum(Payment.amount).label("revenue")
    ).filter(Payment.status == "Completed") \
        .group_by("month").order_by("month").all()

    # Plan generating highest revenue (price * number of memberships sold)
    plan_revenue = db.session.query(
        Plan.plan_name, (Plan.price * func.count(Membership.membership_id)).label("total_revenue")
    ).join(Membership, Membership.plan_id == Plan.plan_id) \
        .group_by(Plan.plan_id, Plan.plan_name, Plan.price) \
        .order_by((Plan.price * func.count(Membership.membership_id)).desc()) \
        .all()

    # Member spending analysis (full ranked list)
    spending = db.session.query(
        Member.member_name, func.coalesce(func.sum(Payment.amount), 0).label("total_spent")
    ).outerjoin(Payment, (Payment.member_id == Member.member_id) & (Payment.status == "Completed")) \
        .group_by(Member.member_id, Member.member_name) \
        .order_by(func.coalesce(func.sum(Payment.amount), 0).desc()) \
        .all()

    # Trainer performance report (members handled)
    trainer_performance = db.session.query(
        Trainer.trainer_name, Trainer.specialization,
        func.count(Member.member_id).label("members_handled")
    ).outerjoin(Member, Member.trainer_id == Trainer.trainer_id) \
        .group_by(Trainer.trainer_id, Trainer.trainer_name, Trainer.specialization) \
        .order_by(func.count(Member.member_id).desc()) \
        .all()

    return render_template(
        "reports/index.html",
        top_plans=top_plans,
        most_active=most_active,
        monthly_revenue=monthly_revenue,
        plan_revenue=plan_revenue,
        spending=spending,
        trainer_performance=trainer_performance,
    )
