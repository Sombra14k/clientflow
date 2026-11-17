# ClientFlow

**Sistema web de gestão de clientes e agendamentos, com painel de indicadores e exportação automática para Excel.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-PostgreSQL-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

O ClientFlow centraliza o cadastro de clientes e a agenda de atendimentos de uma pequena empresa ou profissional autônomo. O projeto foi construído em Python/Flask para demonstrar, na prática, autenticação segura, persistência em banco de dados relacional, CRUD completo, dashboard e automação de relatórios.

## Demonstração

<!-- Adicione prints em docs/screenshots e atualize os caminhos abaixo -->
| Login | Dashboard |
|---|---|
| ![Login](docs/screenshots/login.png) | ![Dashboard](docs/screenshots/dashboard.png) |

> Para testar sem cadastro, clique em **Entrar com conta de demonstração** na tela de login
> (ou use `demo@clientflow.com` / `demo1234`).

## Funcionalidades

- **Autenticação segura:** senhas armazenadas com hash e salt (Werkzeug), sessões com Flask-Login, proteção CSRF em todos os formulários e redirecionamento pós-login validado.
- **Conta de demonstração:** acesso com um clique para avaliação rápida do sistema.
- **CRUD completo:** cadastro, listagem, edição e exclusão de **clientes** e **agendamentos**, com validação de dados.
- **Dashboard:** cards com total de clientes, clientes ativos, atendimentos pendentes e receita concluída no mês; tabela de próximos atendimentos com filtro instantâneo; distribuição de clientes por status.
- **Busca e filtros:** pesquisa por nome, empresa, e-mail, telefone ou título e filtro por status nas listagens.
- **Automação de relatórios:** exportação em **CSV** (compatível com Excel em português) e **Excel (.xlsx)** formatado, incluindo relatório consolidado com duas abas.
- **Interface responsiva:** layout corporativo que se adapta a desktop, tablet e celular.
- **Dados de exemplo:** o banco é populado automaticamente na primeira execução.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Back-end | Python, Flask, Flask-SQLAlchemy, Flask-Login |
| Banco de dados | SQLite (padrão) ou PostgreSQL |
| Exportação | openpyxl, csv |
| Front-end | Jinja2, HTML5, CSS3, JavaScript |
| Testes | pytest |
| Deploy | gunicorn |

## Estrutura do projeto

```
clientflow/
├── run.py                   # ponto de entrada da aplicação
├── config.py                # configurações (SECRET_KEY, DATABASE_URL)
├── requirements.txt
├── app/
│   ├── __init__.py          # application factory, CSRF e filtros de template
│   ├── models.py            # User, Client, Appointment
│   ├── seed.py              # usuário e dados de demonstração
│   ├── routes/              # auth, main (dashboard/export), clients, appointments
│   ├── services/export.py   # geração de CSV e Excel
│   ├── templates/           # páginas HTML (Jinja2)
│   └── static/              # css/ e js/
├── instance/                # banco SQLite (gerado automaticamente)
├── tests/                   # testes automatizados
└── docs/screenshots/        # imagens usadas neste README
```

## Como executar

Pré-requisito: Python 3.10 ou superior.

```bash
git clone https://github.com/SEU-USUARIO/clientflow.git
cd clientflow

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python run.py
```

Acesse **http://127.0.0.1:5000** no navegador.

## Configuração

| Variável | Descrição | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave usada para assinar sessões e tokens CSRF | valor de desenvolvimento |
| `DATABASE_URL` | URL do banco de dados | SQLite em `instance/crm.db` |

Exemplo com PostgreSQL (instale também `psycopg2-binary`):

```bash
export DATABASE_URL="postgresql+psycopg2://usuario:senha@localhost:5432/clientflow"
```

## Testes

```bash
pip install pytest
pytest
```

Os testes cobrem proteção de rotas, login (incluindo senha incorreta e conta demo), CRUD de clientes e exportações.

## Deploy em produção

```bash
export SECRET_KEY="uma-chave-longa-e-aleatoria"
gunicorn run:app
```

Em produção, defina sempre uma `SECRET_KEY` própria, use HTTPS e prefira PostgreSQL. Considere também remover ou desativar a conta de demonstração.

## Rotas principais

| Rota | Descrição |
|---|---|
| `/login` | Autenticação e acesso demo |
| `/` | Dashboard |
| `/clientes/` | Listagem, busca e filtro de clientes |
| `/agendamentos/` | Listagem, busca e filtro de agendamentos |
| `/export/<clientes\|agendamentos>.<csv\|xlsx>` | Exportação de dados |
| `/export/relatorio.xlsx` | Relatório consolidado em Excel |

## Próximos passos

- [ ] Paginação das listagens
- [ ] Gráficos de receita por período
- [ ] Lembretes de agendamento por e-mail
- [ ] Gestão de múltiplos usuários e permissões
- [ ] Containerização com Docker

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).

## Autor

Desenvolvido por **Jhonatan de Jesus Rodrigues** — [LinkedIn](https://www.linkedin.com/in/jhonatan-de-jesus/) · [GitHub](https://github.com/Sombra14k)
