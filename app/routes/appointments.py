from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import or_

from app import db
from app.models import APPOINTMENT_STATUS, Appointment, Client

bp = Blueprint("appointments", __name__, url_prefix="/agendamentos")


def _fill(appt):
    f = request.form
    title = f.get("title", "").strip()
    client = db.session.get(Client, int(f["client_id"])) if f.get("client_id", "").isdigit() else None
    try:
        when = datetime.strptime(f.get("scheduled_at", ""), "%Y-%m-%dT%H:%M")
    except ValueError:
        when = None
    try:
        value = float(f.get("value", "0").replace(",", ".") or 0)
    except ValueError:
        value = None
    if not title or not client or not when or value is None or value < 0:
        flash("Preencha cliente, título, data/hora e um valor válido.", "error")
        return False
    appt.client_id, appt.title, appt.scheduled_at, appt.value = client.id, title, when, value
    appt.status = f.get("status") if f.get("status") in APPOINTMENT_STATUS else "Pendente"
    appt.notes = f.get("notes", "").strip()
    return True


def _form(appt, editing):
    return render_template("appointments/form.html", appt=appt, editing=editing,
                           clients=Client.query.order_by(Client.name).all(),
                           statuses=APPOINTMENT_STATUS)


@bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    query = Appointment.query.join(Client)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Appointment.title.ilike(like), Client.name.ilike(like),
                                 Client.company.ilike(like)))
    if status in APPOINTMENT_STATUS:
        query = query.filter(Appointment.status == status)
    return render_template("appointments/list.html",
                           appointments=query.order_by(Appointment.scheduled_at.desc()).all(),
                           q=q, status=status, statuses=APPOINTMENT_STATUS)


@bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    appt = Appointment(scheduled_at=datetime.now())
    if request.method == "POST" and _fill(appt):
        db.session.add(appt)
        db.session.commit()
        flash("Agendamento criado.", "ok")
        return redirect(url_for("appointments.index"))
    return _form(appt, False)


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def edit(id):
    appt = db.get_or_404(Appointment, id)
    if request.method == "POST" and _fill(appt):
        db.session.commit()
        flash("Agendamento atualizado.", "ok")
        return redirect(url_for("appointments.index"))
    return _form(appt, True)


@bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def delete(id):
    db.session.delete(db.get_or_404(Appointment, id))
    db.session.commit()
    flash("Agendamento excluído.", "ok")
    return redirect(url_for("appointments.index"))
