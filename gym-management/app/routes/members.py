from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Member, Trainer, Plan, Membership

members_bp = Blueprint("members", __name__, url_prefix="/members")


@members_bp.route("/")
@login_required
def list_members():
    q = request.args.get("q", "").strip()
    query = Member.query
    if q:
        query = query.filter(Member.member_name.ilike(f"%{q}%"))
    members = query.order_by(Member.member_id.desc()).all()
    return render_template("members/list.html", members=members, q=q)


@members_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_member():
    trainers = Trainer.query.all()
    plans = Plan.query.all()
    if request.method == "POST":
        member = Member(
            member_name=request.form["member_name"],
            email=request.form.get("email") or None,
            phone=request.form.get("phone"),
            join_date=_parse_date(request.form.get("join_date")) or datetime.today().date(),
            trainer_id=request.form.get("trainer_id") or None,
        )
        db.session.add(member)
        db.session.flush()

        plan_id = request.form.get("plan_id")
        if plan_id:
            plan = Plan.query.get(int(plan_id))
            start = datetime.today().date()
            end = start + timedelta(days=plan.duration)
            db.session.add(Membership(member_id=member.member_id, plan_id=plan.plan_id,
                                       start_date=start, end_date=end))

        db.session.commit()
        flash("Member added successfully", "success")
        return redirect(url_for("members.list_members"))

    return render_template("members/form.html", member=None, trainers=trainers, plans=plans)


@members_bp.route("/<int:member_id>/edit", methods=["GET", "POST"])
@login_required
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)
    trainers = Trainer.query.all()
    plans = Plan.query.all()

    if request.method == "POST":
        member.member_name = request.form["member_name"]
        member.email = request.form.get("email") or None
        member.phone = request.form.get("phone")
        member.join_date = _parse_date(request.form.get("join_date")) or member.join_date
        member.trainer_id = request.form.get("trainer_id") or None
        db.session.commit()
        flash("Member updated", "success")
        return redirect(url_for("members.list_members"))

    return render_template("members/form.html", member=member, trainers=trainers, plans=plans)


@members_bp.route("/<int:member_id>/delete", methods=["POST"])
@login_required
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash("Member deleted", "info")
    return redirect(url_for("members.list_members"))


@members_bp.route("/<int:member_id>/renew", methods=["POST"])
@login_required
def renew_membership(member_id):
    member = Member.query.get_or_404(member_id)
    plan_id = request.form.get("plan_id")
    plan = Plan.query.get_or_404(int(plan_id))
    start = datetime.today().date()
    end = start + timedelta(days=plan.duration)
    db.session.add(Membership(member_id=member.member_id, plan_id=plan.plan_id,
                               start_date=start, end_date=end))
    db.session.commit()
    flash(f"Membership renewed with plan: {plan.plan_name}", "success")
    return redirect(url_for("members.view_member", member_id=member.member_id))


@members_bp.route("/<int:member_id>")
@login_required
def view_member(member_id):
    member = Member.query.get_or_404(member_id)
    plans = Plan.query.all()
    return render_template("members/view.html", member=member, plans=plans)


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()
