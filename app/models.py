from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_demo = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        # PBKDF2/scrypt com salt: a senha nunca é salva em texto puro
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


CLIENT_STATUS = ["Lead", "Ativo", "Inativo"]
APPOINTMENT_STATUS = ["Pendente", "Confirmado", "Concluído", "Cancelado"]

BADGE = {
    "Lead": "info", "Ativo": "ok", "Inativo": "muted",
    "Pendente": "warn", "Confirmado": "info", "Concluído": "ok", "Cancelado": "muted",
}


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120))
    email = db.Column(db.String(160))
    phone = db.Column(db.String(30))
    status = db.Column(db.String(20), default="Lead", nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointments = db.relationship(
        "Appointment", backref="client", cascade="all, delete-orphan", lazy="select"
    )

    @property
    def badge(self):
        return BADGE.get(self.status, "muted")


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(20), default="Pendente", nullable=False)
    value = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)

    @property
    def badge(self):
        return BADGE.get(self.status, "muted")
