import secrets

from flask import Flask, abort, request, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar o sistema."


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import bp as auth_bp
    from app.routes.main import bp as main_bp
    from app.routes.clients import bp as clients_bp
    from app.routes.appointments import bp as appointments_bp

    for bp in (auth_bp, main_bp, clients_bp, appointments_bp):
        app.register_blueprint(bp)

    # --- Proteção CSRF simples baseada em sessão ---------------------------
    def csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(16)
        return session["csrf_token"]

    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.before_request
    def check_csrf():
        if request.method == "POST":
            sent = request.form.get("csrf_token", "")
            if not sent or not secrets.compare_digest(sent, session.get("csrf_token", "")):
                abort(400, "Token CSRF inválido. Recarregue a página e tente novamente.")

    @app.template_filter("dt")
    def fmt_dt(value):
        return value.strftime("%d/%m/%Y %H:%M") if value else "—"

    @app.template_filter("brl")
    def fmt_brl(value):
        value = value or 0
        return "R$ " + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    with app.app_context():
        from app.seed import seed_demo

        db.create_all()
        seed_demo()

    return app
