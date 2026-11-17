from datetime import datetime, timedelta

from app import db
from app.models import Appointment, Client, User

DEMO_EMAIL = "demo@clientflow.com"
DEMO_PASSWORD = "demo1234"

CLIENTS = [
    ("Mariana Alves", "Alves & Costa Advocacia", "Ativo"),
    ("Rafael Nogueira", "Nogueira Engenharia", "Ativo"),
    ("Camila Rocha", "Studio Rocha Design", "Lead"),
    ("Eduardo Martins", "Martins Logística", "Ativo"),
    ("Juliana Prado", "Clínica Prado Saúde", "Ativo"),
    ("Thiago Barbosa", "TB Soluções Digitais", "Lead"),
    ("Fernanda Lima", "Lima Contabilidade", "Inativo"),
    ("Gustavo Ribeiro", "Ribeiro Materiais", "Ativo"),
    ("Patrícia Souza", "Souza Eventos", "Lead"),
    ("Bruno Carvalho", "Carvalho Autopeças", "Ativo"),
    ("Aline Teixeira", "Teixeira Odontologia", "Inativo"),
    ("Diego Fernandes", "DF Consultoria", "Ativo"),
]

TITLES = [
    ("Reunião de diagnóstico", 0), ("Apresentação de proposta", 0),
    ("Revisão mensal de contrato", 1800), ("Treinamento da equipe", 2400),
    ("Visita técnica", 950), ("Alinhamento de escopo", 0),
]


def seed_demo():
    """Cria usuário e dados de demonstração apenas se o banco estiver vazio."""
    if not User.query.filter_by(email=DEMO_EMAIL).first():
        user = User(name="Conta de Demonstração", email=DEMO_EMAIL, is_demo=True)
        user.set_password(DEMO_PASSWORD)
        db.session.add(user)

    if Client.query.count() == 0:
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        for i, (name, company, status) in enumerate(CLIENTS):
            slug = name.lower().split()[0].replace("í", "i")
            c = Client(
                name=name, company=company, status=status,
                email=f"{slug}@exemplo.com.br", phone=f"(11) 9{8000 + i * 37:04d}-{1200 + i * 91:04d}",
                notes="Cliente de demonstração.", created_at=now - timedelta(days=40 - i * 3),
            )
            db.session.add(c)
            db.session.flush()
            for j in range(2):
                title, value = TITLES[(i + j * 2) % len(TITLES)]
                offset = (i * 2 + j * 5) - 14
                when = now + timedelta(days=offset, hours=(i + j) % 8)
                status = "Concluído" if offset < 0 else ("Confirmado" if offset % 2 else "Pendente")
                if offset < 0 and i % 5 == 0:
                    status = "Cancelado"
                db.session.add(Appointment(
                    client_id=c.id, title=title, scheduled_at=when, status=status, value=value,
                ))
    db.session.commit()
