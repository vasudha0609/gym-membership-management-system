from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Payment, Member

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.route("/")
@login_required
def list_payments():
    payments = Payment.query.order_by(Payment.payment_id.desc()).all()
    return render_template("payments/list.html", payments=payments)


@payments_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_payment():
    members = Member.query.all()
    if request.method == "POST":
        payment = Payment(
            member_id=int(request.form["member_id"]),
            amount=float(request.form["amount"]),
            status=request.form.get("status", "Completed"),
        )
        db.session.add(payment)
        db.session.commit()
        flash("Payment recorded", "success")
        return redirect(url_for("payments.list_payments"))
    return render_template("payments/form.html", members=members)


@payments_bp.route("/<int:payment_id>/delete", methods=["POST"])
@login_required
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    flash("Payment record deleted", "info")
    return redirect(url_for("payments.list_payments"))
