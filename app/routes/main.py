from datetime import datetime

from flask import Blueprint, abort, render_template
from flask_login import login_required
from sqlalchemy import func

from app import db
from app.models import CLIENT_STATUS, Appointment, Client
from app.services import export

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def dashboard():
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    revenue = (
        db.session.query(func.coalesce(func.sum(Appointment.value), 0))
        .filter(Appointment.status == "Concluído", Appointment.scheduled_at >= month_start)
        .scalar()
    )
    stats = {
        "clients": Client.query.count(),
        "active": Client.query.filter_by(status="Ativo").count(),
        "pending": Appointment.query.filter_by(status="Pendente").count(),
        "revenue": revenue,
    }
    by_status = {s: Client.query.filter_by(status=s).count() for s in CLIENT_STATUS}
    upcoming = (
        Appointment.query.filter(
            Appointment.scheduled_at >= now, Appointment.status.in_(["Pendente", "Confirmado"])
        )
        .order_by(Appointment.scheduled_at).limit(8).all()
    )
    return render_template(
        "dashboard.html", stats=stats, by_status=by_status, upcoming=upcoming,
        total=max(stats["clients"], 1),
    )


@bp.route("/export/<entity>.<fmt>")
@login_required
def export_data(entity, fmt):
    """Automação: gera CSV ou planilha Excel formatada com um clique."""
    if entity not in ("clientes", "agendamentos", "relatorio") or fmt not in ("csv", "xlsx"):
        abort(404)
    if entity == "relatorio" and fmt == "csv":
        abort(404)
    return export.build_response(entity, fmt)
