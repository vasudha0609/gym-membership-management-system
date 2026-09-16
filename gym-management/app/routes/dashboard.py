from datetime import date, timedelta
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from app import db
from app.models import Member, Payment, Membership

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    total_members = Member.query.count()
    active_members = sum(1 for m in Member.query.all() if m.membership_status == "Active")

    total_revenue = db.session.query(func.coalesce(func.sum(Payment.amount), 0)) \
        .filter(Payment.status == "Completed").scalar()

    this_month_start = date.today().replace(day=1)
    month_revenue = db.session.query(func.coalesce(func.sum(Payment.amount), 0)) \
        .filter(Payment.status == "Completed", Payment.payment_date >= this_month_start).scalar()

    soon = date.today() + timedelta(days=7)
    expiring_soon = Membership.query.filter(
        Membership.end_date >= date.today(),
        Membership.end_date <= soon
    ).all()

    recent_members = Member.query.order_by(Member.member_id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_members=total_members,
        active_members=active_members,
        total_revenue=total_revenue,
        month_revenue=month_revenue,
        expiring_soon=expiring_soon,
        recent_members=recent_members,
    )
