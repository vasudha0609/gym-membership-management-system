from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Trainer

trainers_bp = Blueprint("trainers", __name__, url_prefix="/trainers")


@trainers_bp.route("/")
@login_required
def list_trainers():
    trainers = Trainer.query.all()
    return render_template("trainers/list.html", trainers=trainers)


@trainers_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_trainer():
    if request.method == "POST":
        trainer = Trainer(
            trainer_name=request.form["trainer_name"],
            specialization=request.form.get("specialization"),
            phone=request.form.get("phone"),
        )
        db.session.add(trainer)
        db.session.commit()
        flash("Trainer added", "success")
        return redirect(url_for("trainers.list_trainers"))
    return render_template("trainers/form.html", trainer=None)


@trainers_bp.route("/<int:trainer_id>/edit", methods=["GET", "POST"])
@login_required
def edit_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    if request.method == "POST":
        trainer.trainer_name = request.form["trainer_name"]
        trainer.specialization = request.form.get("specialization")
        trainer.phone = request.form.get("phone")
        db.session.commit()
        flash("Trainer updated", "success")
        return redirect(url_for("trainers.list_trainers"))
    return render_template("trainers/form.html", trainer=trainer)


@trainers_bp.route("/<int:trainer_id>/delete", methods=["POST"])
@login_required
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    db.session.delete(trainer)
    db.session.commit()
    flash("Trainer deleted", "info")
    return redirect(url_for("trainers.list_trainers"))
