from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User
from app.seed import DEMO_EMAIL

bp = Blueprint("auth", __name__)


def _safe_next(target):
    return target if target and target.startswith("/") and not target.startswith("//") else None


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user)
            return redirect(_safe_next(request.args.get("next")) or url_for("main.dashboard"))
        flash("E-mail ou senha incorretos.", "error")
    return render_template("auth/login.html", demo_email=DEMO_EMAIL)


@bp.route("/demo-login", methods=["POST"])
def demo_login():
    user = User.query.filter_by(email=DEMO_EMAIL).first()
    if not user:
        flash("Conta de demonstração indisponível.", "error")
        return redirect(url_for("auth.login"))
    login_user(user)
    return redirect(url_for("main.dashboard"))


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "ok")
    return redirect(url_for("auth.login"))
