import csv
import io
from datetime import datetime

from flask import Response
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from app.models import Appointment, Client

CLIENT_HEAD = ["ID", "Nome", "Empresa", "E-mail", "Telefone", "Status", "Cadastro", "Observações"]
APPT_HEAD = ["ID", "Cliente", "Título", "Data/Hora", "Status", "Valor (R$)", "Observações"]


def client_rows():
    return [[c.id, c.name, c.company, c.email, c.phone, c.status,
             c.created_at.strftime("%d/%m/%Y"), c.notes]
            for c in Client.query.order_by(Client.name)]


def appt_rows():
    return [[a.id, a.client.name, a.title, a.scheduled_at.strftime("%d/%m/%Y %H:%M"),
             a.status, a.value, a.notes]
            for a in Appointment.query.order_by(Appointment.scheduled_at)]


def _sheet(ws, head, rows):
    ws.append(head)
    for r in rows:
        ws.append(r)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="14213D")
        cell.alignment = Alignment(vertical="center")
    for i, col in enumerate(zip(head, *rows), start=1):
        width = max(len(str(v)) if v is not None else 0 for v in col)
        ws.column_dimensions[get_column_letter(i)].width = min(max(width + 3, 10), 45)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def build_response(entity, fmt):
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{entity}_{stamp}.{fmt}"
    if fmt == "csv":
        head, rows = (CLIENT_HEAD, client_rows()) if entity == "clientes" else (APPT_HEAD, appt_rows())
        buf = io.StringIO()
        w = csv.writer(buf, delimiter=";")  # ponto e vírgula abre direto no Excel pt-BR
        w.writerow(head)
        w.writerows(rows)
        data = ("\ufeff" + buf.getvalue()).encode("utf-8")
        mime = "text/csv; charset=utf-8"
    else:
        wb = Workbook()
        wb.remove(wb.active)
        if entity in ("clientes", "relatorio"):
            _sheet(wb.create_sheet("Clientes"), CLIENT_HEAD, client_rows())
        if entity in ("agendamentos", "relatorio"):
            _sheet(wb.create_sheet("Agendamentos"), APPT_HEAD, appt_rows())
        out = io.BytesIO()
        wb.save(out)
        data = out.getvalue()
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return Response(data, mimetype=mime,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})
