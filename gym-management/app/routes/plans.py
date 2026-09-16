from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Plan

plans_bp = Blueprint("plans", __name__, url_prefix="/plans")


@plans_bp.route("/")
@login_required
def list_plans():
    plans = Plan.query.all()
    return render_template("plans/list.html", plans=plans)


@plans_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_plan():
    if request.method == "POST":
        plan = Plan(
            plan_name=request.form["plan_name"],
            duration=int(request.form["duration"]),
            price=float(request.form["price"]),
        )
        db.session.add(plan)
        db.session.commit()
        flash("Plan created", "success")
        return redirect(url_for("plans.list_plans"))
    return render_template("plans/form.html", plan=None)


@plans_bp.route("/<int:plan_id>/edit", methods=["GET", "POST"])
@login_required
def edit_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    if request.method == "POST":
        plan.plan_name = request.form["plan_name"]
        plan.duration = int(request.form["duration"])
        plan.price = float(request.form["price"])
        db.session.commit()
        flash("Plan updated", "success")
        return redirect(url_for("plans.list_plans"))
    return render_template("plans/form.html", plan=plan)


@plans_bp.route("/<int:plan_id>/delete", methods=["POST"])
@login_required
def delete_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    flash("Plan deleted", "info")
    return redirect(url_for("plans.list_plans"))
