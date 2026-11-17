from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import or_

from app import db
from app.models import CLIENT_STATUS, Client

bp = Blueprint("clients", __name__, url_prefix="/clientes")


def _fill(client):
    f = request.form
    name = f.get("name", "").strip()
    email = f.get("email", "").strip()
    if not name:
        flash("Informe o nome do cliente.", "error")
        return False
    if email and ("@" not in email or "." not in email.split("@")[-1]):
        flash("Informe um e-mail válido.", "error")
        return False
    client.name = name
    client.company = f.get("company", "").strip()
    client.email = email
    client.phone = f.get("phone", "").strip()
    client.status = f.get("status") if f.get("status") in CLIENT_STATUS else "Lead"
    client.notes = f.get("notes", "").strip()
    return True


@bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    query = Client.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Client.name.ilike(like), Client.company.ilike(like),
                                 Client.email.ilike(like), Client.phone.ilike(like)))
    if status in CLIENT_STATUS:
        query = query.filter_by(status=status)
    return render_template("clients/list.html", clients=query.order_by(Client.name).all(),
                           q=q, status=status, statuses=CLIENT_STATUS)


@bp.route("/novo", methods=["GET", "POST"])
@login_required
def create():
    client = Client()
    if request.method == "POST" and _fill(client):
        db.session.add(client)
        db.session.commit()
        flash("Cliente cadastrado.", "ok")
        return redirect(url_for("clients.index"))
    return render_template("clients/form.html", client=client, statuses=CLIENT_STATUS, editing=False)


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def edit(id):
    client = db.get_or_404(Client, id)
    if request.method == "POST" and _fill(client):
        db.session.commit()
        flash("Cliente atualizado.", "ok")
        return redirect(url_for("clients.index"))
    return render_template("clients/form.html", client=client, statuses=CLIENT_STATUS, editing=True)


@bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def delete(id):
    client = db.get_or_404(Client, id)
    db.session.delete(client)
    db.session.commit()
    flash("Cliente excluído junto com seus agendamentos.", "ok")
    return redirect(url_for("clients.index"))
