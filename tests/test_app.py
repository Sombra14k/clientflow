import re

import pytest

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture()
def client():
    app = create_app(TestConfig)
    with app.test_client() as c:
        yield c


def token(c, path="/login"):
    html = c.get(path).get_data(as_text=True)
    return re.search(r'name="csrf_token" value="(\w+)"', html).group(1)


def demo_login(c):
    return c.post("/demo-login", data={"csrf_token": token(c)}, follow_redirects=True)


def test_requires_login(client):
    assert client.get("/").status_code == 302


def test_wrong_password(client):
    r = client.post("/login", data={"csrf_token": token(client), "email": "demo@clientflow.com", "password": "x"})
    assert "incorretos" in r.get_data(as_text=True)


def test_demo_login_and_dashboard(client):
    r = demo_login(client)
    assert "Visão geral" in r.get_data(as_text=True)


def test_client_crud(client):
    demo_login(client)
    t = token(client, "/clientes/novo")
    client.post("/clientes/novo", data={"csrf_token": t, "name": "Teste CRUD", "status": "Ativo"})
    assert "Teste CRUD" in client.get("/clientes/?q=CRUD").get_data(as_text=True)
    client.post("/clientes/13/editar", data={"csrf_token": t, "name": "Teste Editado", "status": "Lead"})
    assert "Teste Editado" in client.get("/clientes/").get_data(as_text=True)
    client.post("/clientes/13/excluir", data={"csrf_token": t})
    assert "Teste Editado" not in client.get("/clientes/").get_data(as_text=True)


def test_exports(client):
    demo_login(client)
    assert client.get("/export/clientes.csv").mimetype == "text/csv"
    assert client.get("/export/relatorio.xlsx").status_code == 200
