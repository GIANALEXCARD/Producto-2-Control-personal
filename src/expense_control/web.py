from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import ClassVar, override
from urllib.parse import parse_qs, urlencode, urlparse

from .domain import Transaction, TransactionLedger, TransactionType
from .repository import SQLiteTransactionRepository


DEFAULT_DATABASE_PATH = Path("data") / "expense-control.sqlite3"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


@dataclass(frozen=True, slots=True)
class WebAppConfig:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    database_path: Path = DEFAULT_DATABASE_PATH


@dataclass(frozen=True, slots=True)
class PageState:
    selected_type: str = ""
    selected_category: str = ""
    message: str = ""
    error: str = ""


class ExpenseControlRequestHandler(BaseHTTPRequestHandler):
    repository: ClassVar[SQLiteTransactionRepository]

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        if parsed_url.path != "/":
            self._send_not_found()
            return

        query_values = parse_qs(parsed_url.query)
        state = PageState(
            selected_type=_first_query_value(query_values, "type"),
            selected_category=_first_query_value(query_values, "category"),
            message=_first_query_value(query_values, "message"),
        )
        self._send_page(state)

    def do_POST(self) -> None:
        parsed_url = urlparse(self.path)
        if parsed_url.path != "/transactions":
            self._send_not_found()
            return

        try:
            form_values = self._read_form_values()
            transaction = _transaction_from_form(form_values)
            _ = self.repository.save_transaction(transaction)
        except (TypeError, ValueError) as error:
            state = PageState(error=str(error))
            self._send_page(state, status=HTTPStatus.BAD_REQUEST)
            return

        self._redirect(f"/?{urlencode({'message': 'Movimiento registrado correctamente.'})}")

    @override
    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_form_values(self) -> dict[str, str]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        parsed_values = parse_qs(raw_body, keep_blank_values=True)
        return {
            field_name: values[0]
            for field_name, values in parsed_values.items()
            if values
        }

    def _send_page(self, state: PageState, status: HTTPStatus = HTTPStatus.OK) -> None:
        transactions = self.repository.list_transactions()
        ledger = TransactionLedger(transactions)
        filtered_transactions = _filter_transactions(transactions, state)
        categories = _unique_categories(transactions)
        html = render_dashboard(
            ledger=ledger,
            transactions=filtered_transactions,
            categories=categories,
            state=state,
        )
        encoded_html = html.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded_html)))
        self.end_headers()
        _ = self.wfile.write(encoded_html)

    def _send_not_found(self) -> None:
        body = b"Not found"
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        _ = self.wfile.write(body)

    def _redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()


def create_server(config: WebAppConfig) -> ThreadingHTTPServer:
    repository = SQLiteTransactionRepository(config.database_path)

    class ConfiguredExpenseControlRequestHandler(ExpenseControlRequestHandler):
        pass

    ConfiguredExpenseControlRequestHandler.repository = repository
    return ThreadingHTTPServer((config.host, config.port), ConfiguredExpenseControlRequestHandler)


def serve(config: WebAppConfig) -> None:
    with create_server(config) as server:
        address, port = server.server_address[:2]
        print(f"Expense Control disponible en http://{address}:{port}")
        print(f"Base de datos SQLite: {config.database_path}")
        server.serve_forever()


def render_dashboard(
    *,
    ledger: TransactionLedger,
    transactions: list[Transaction],
    categories: list[str],
    state: PageState,
) -> str:
    balance = ledger.balance()
    balance_modifier = "positive" if balance >= 0 else "negative"
    today = date.today().isoformat()
    message_html = _render_notice(state.message, "success") if state.message else ""
    error_html = _render_notice(state.error, "error") if state.error else ""
    transaction_rows = _render_transaction_rows(transactions)
    category_options = _render_category_options(categories, state.selected_category)

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Expense Control</title>
  <style>
    :root {{
      --color-ink: hsl(143 14% 11%);
      --color-muted: hsl(128 4% 45%);
      --color-paper: hsl(40 100% 97%);
      --color-panel: hsl(40 100% 99%);
      --color-panel-soft: hsl(38 53% 90%);
      --color-primary: hsl(152 56% 28%);
      --color-primary-dark: hsl(153 56% 19%);
      --color-accent: hsl(33 70% 50%);
      --color-income: hsl(151 55% 31%);
      --color-expense: hsl(8 50% 48%);
      --color-border: hsl(35 37% 80%);
      --color-shadow: rgba(51, 38, 19, 0.16);
      --color-surface-glass: rgba(255, 253, 248, 0.88);
      --color-balance-glow: rgba(217, 137, 40, 0.65);
      --color-balance-text: rgba(255, 253, 248, 0.75);
      --color-grid-line: rgba(25, 33, 29, 0.05);
      --color-hero-glow: rgba(217, 137, 40, 0.22);
      --color-page-mist: hsl(80 32% 93%);
      --color-page-sand: hsl(38 39% 82%);
      --color-focus: rgba(31, 111, 74, 0.18);
      --color-primary-shadow: rgba(31, 111, 74, 0.2);
      --color-success-soft: rgba(35, 122, 84, 0.14);
      --color-error-soft: rgba(184, 77, 61, 0.14);
      --space-1: 0.25rem;
      --space-2: 0.5rem;
      --space-3: 0.75rem;
      --space-4: 1rem;
      --space-5: 1.5rem;
      --space-6: 2rem;
      --space-7: 3rem;
      --radius-sm: 0.75rem;
      --radius-md: 1.25rem;
      --radius-lg: 2rem;
      --radius-pill: 999px;
      --blur-panel: 0.75rem;
      --shadow-card: 0 1.25rem 3rem var(--color-shadow);
      --font-title: Georgia, 'Times New Roman', serif;
      --font-body: 'Trebuchet MS', Verdana, sans-serif;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--color-ink);
      font-family: var(--font-body);
      background:
        radial-gradient(circle at top left, var(--color-hero-glow), transparent 24rem),
        linear-gradient(135deg, var(--color-paper), var(--color-page-mist) 58%, var(--color-page-sand));
    }}

    body::before {{
      position: fixed;
      inset: 0;
      pointer-events: none;
      content: "";
      opacity: 0.45;
      background-image: linear-gradient(var(--color-grid-line) 1px, transparent 1px), linear-gradient(90deg, var(--color-grid-line) 1px, transparent 1px);
      background-size: var(--space-6) var(--space-6);
    }}

    .shell {{
      position: relative;
      width: min(72rem, calc(100% - var(--space-5)));
      margin: 0 auto;
      padding: var(--space-7) 0;
    }}

    .hero {{
      display: grid;
      grid-template-columns: 1.25fr 0.75fr;
      gap: var(--space-5);
      align-items: stretch;
      margin-bottom: var(--space-5);
    }}

    .hero-card,
    .panel,
    .metric-card {{
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      background: var(--color-surface-glass);
      box-shadow: var(--shadow-card);
      backdrop-filter: blur(var(--blur-panel));
    }}

    .hero-card {{
      padding: var(--space-7);
      overflow: hidden;
    }}

    .eyebrow {{
      margin: 0 0 var(--space-3);
      color: var(--color-primary);
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}

    h1,
    h2,
    h3 {{
      margin: 0;
      font-family: var(--font-title);
      line-height: 1;
    }}

    h1 {{
      max-width: 12ch;
      font-size: clamp(2.75rem, 8vw, 5.5rem);
      letter-spacing: -0.06em;
    }}

    h2 {{ font-size: clamp(1.75rem, 3vw, 2.5rem); }}
    h3 {{ font-size: 1.2rem; }}

    .hero-copy {{
      max-width: 36rem;
      margin: var(--space-5) 0 0;
      color: var(--color-muted);
      font-size: 1.05rem;
      line-height: 1.7;
    }}

    .balance-card {{
      display: flex;
      min-height: 18rem;
      flex-direction: column;
      justify-content: space-between;
      padding: var(--space-6);
      color: var(--color-panel);
      border-radius: var(--radius-lg);
      background:
        radial-gradient(circle at top right, var(--color-balance-glow), transparent 12rem),
        linear-gradient(145deg, var(--color-primary-dark), var(--color-primary));
      box-shadow: var(--shadow-card);
    }}

    .balance-card span {{ color: var(--color-balance-text); }}
    .balance-card strong {{ font-family: var(--font-title); font-size: clamp(2.5rem, 5vw, 4.5rem); }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: var(--space-5);
      margin-bottom: var(--space-5);
    }}

    .metric-card {{ padding: var(--space-5); }}
    .metric-label {{ margin: 0 0 var(--space-2); color: var(--color-muted); }}
    .metric-value {{ margin: 0; font-family: var(--font-title); font-size: 2.25rem; }}
    .metric-value.income {{ color: var(--color-income); }}
    .metric-value.expense {{ color: var(--color-expense); }}

    .grid {{
      display: grid;
      grid-template-columns: minmax(18rem, 0.75fr) minmax(0, 1.25fr);
      gap: var(--space-5);
      align-items: start;
    }}

    .panel {{ padding: var(--space-5); }}
    .panel-header {{ display: flex; justify-content: space-between; gap: var(--space-3); align-items: end; margin-bottom: var(--space-5); }}
    .panel-subtitle {{ margin: var(--space-2) 0 0; color: var(--color-muted); line-height: 1.5; }}

    .form-grid {{ display: grid; gap: var(--space-4); }}
    .field {{ display: grid; gap: var(--space-2); }}
    .field label {{ font-size: 0.84rem; font-weight: 700; color: var(--color-muted); text-transform: uppercase; letter-spacing: 0.08em; }}
    .input,
    .select {{
      width: 100%;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-sm);
      padding: var(--space-3) var(--space-4);
      color: var(--color-ink);
      font: inherit;
      background: var(--color-panel);
    }}

    .input:focus,
    .select:focus {{
      outline: 3px solid var(--color-focus);
      border-color: var(--color-primary);
    }}

    .button {{
      border: 0;
      border-radius: var(--radius-sm);
      padding: var(--space-4) var(--space-5);
      color: var(--color-panel);
      font: inherit;
      font-weight: 700;
      cursor: pointer;
      background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
      box-shadow: 0 var(--space-3) var(--space-5) var(--color-primary-shadow);
    }}

    .button:hover {{ transform: translateY(calc(-1 * var(--space-1))); }}
    .button.secondary {{ color: var(--color-primary-dark); background: var(--color-panel-soft); box-shadow: none; text-decoration: none; text-align: center; }}

    .notice {{ margin-bottom: var(--space-4); padding: var(--space-3) var(--space-4); border-radius: var(--radius-sm); font-weight: 700; }}
    .notice.success {{ color: var(--color-primary-dark); background: var(--color-success-soft); }}
    .notice.error {{ color: var(--color-expense); background: var(--color-error-soft); }}

    .filters {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-3); margin-bottom: var(--space-5); }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th,
    td {{ padding: var(--space-3); border-bottom: 1px solid var(--color-border); text-align: left; vertical-align: top; }}
    th {{ color: var(--color-muted); font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }}
    .amount {{ font-weight: 800; white-space: nowrap; }}
    .amount.income {{ color: var(--color-income); }}
    .amount.expense {{ color: var(--color-expense); }}
    .pill {{ display: inline-block; padding: var(--space-1) var(--space-2); border-radius: var(--radius-pill); background: var(--color-panel-soft); font-size: 0.82rem; font-weight: 700; }}
    .empty {{ padding: var(--space-6); border: 1px dashed var(--color-border); border-radius: var(--radius-md); color: var(--color-muted); text-align: center; }}

    @media (max-width: 860px) {{
      .hero,
      .grid,
      .metrics {{ grid-template-columns: 1fr; }}
      .filters {{ grid-template-columns: 1fr; }}
      .hero-card {{ padding: var(--space-6); }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero" aria-labelledby="page-title">
      <div class="hero-card">
        <p class="eyebrow">Producto 2 · Control personal</p>
        <h1 id="page-title">Expense Control</h1>
        <p class="hero-copy">Dashboard académico para registrar ingresos, gastos y revisar el balance personal con persistencia SQLite local.</p>
      </div>
      <aside class="balance-card" aria-label="Balance actual">
        <span>Balance disponible</span>
        <strong class="{balance_modifier}">{_format_money(balance)}</strong>
        <span>{len(ledger.transactions)} movimientos registrados</span>
      </aside>
    </section>

    <section class="metrics" aria-label="Resumen financiero">
      <article class="metric-card">
        <p class="metric-label">Ingresos totales</p>
        <p class="metric-value income">{_format_money(ledger.total_income())}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">Gastos totales</p>
        <p class="metric-value expense">{_format_money(ledger.total_expenses())}</p>
      </article>
    </section>

    <section class="grid">
      <article class="panel" aria-labelledby="form-title">
        <div class="panel-header">
          <div>
            <p class="eyebrow">Nuevo movimiento</p>
            <h2 id="form-title">Registrar</h2>
          </div>
        </div>
        {message_html}
        {error_html}
        <form class="form-grid" method="post" action="/transactions">
          <div class="field">
            <label for="transaction_type">Tipo</label>
            <select class="select" id="transaction_type" name="transaction_type" required>
              <option value="income">Ingreso</option>
              <option value="expense">Gasto</option>
            </select>
          </div>
          <div class="field">
            <label for="amount">Monto</label>
            <input class="input" id="amount" name="amount" type="number" min="0.01" step="0.01" placeholder="120.50" required>
          </div>
          <div class="field">
            <label for="category">Categoría</label>
            <input class="input" id="category" name="category" type="text" maxlength="60" placeholder="Alimentación" required>
          </div>
          <div class="field">
            <label for="description">Descripción</label>
            <input class="input" id="description" name="description" type="text" maxlength="120" placeholder="Compra semanal">
          </div>
          <div class="field">
            <label for="transaction_date">Fecha</label>
            <input class="input" id="transaction_date" name="transaction_date" type="date" value="{today}" required>
          </div>
          <button class="button" type="submit">Guardar movimiento</button>
        </form>
      </article>

      <article class="panel" aria-labelledby="transactions-title">
        <div class="panel-header">
          <div>
            <p class="eyebrow">Historial</p>
            <h2 id="transactions-title">Movimientos</h2>
            <p class="panel-subtitle">Filtra por tipo o categoría para explicar rápidamente el comportamiento del balance durante la demo.</p>
          </div>
        </div>
        <form class="filters" method="get" action="/">
          <div class="field">
            <label for="type">Tipo</label>
            <select class="select" id="type" name="type">
              {_render_type_option('', 'Todos', state.selected_type)}
              {_render_type_option(TransactionType.INCOME.value, 'Ingresos', state.selected_type)}
              {_render_type_option(TransactionType.EXPENSE.value, 'Gastos', state.selected_type)}
            </select>
          </div>
          <div class="field">
            <label for="category_filter">Categoría</label>
            <select class="select" id="category_filter" name="category">
              <option value="">Todas</option>
              {category_options}
            </select>
          </div>
          <button class="button" type="submit">Aplicar filtros</button>
          <a class="button secondary" href="/">Limpiar</a>
        </form>
        {transaction_rows}
      </article>
    </section>
  </main>
</body>
</html>"""


def _transaction_from_form(form_values: dict[str, str]) -> Transaction:
    amount = float(_required_form_value(form_values, "amount", "El monto es obligatorio."))
    transaction_date = date.fromisoformat(
        _required_form_value(form_values, "transaction_date", "La fecha es obligatoria.")
    )
    return Transaction(
        transaction_type=_required_form_value(form_values, "transaction_type", "El tipo es obligatorio."),
        amount=amount,
        category=_required_form_value(form_values, "category", "La categoría es obligatoria."),
        description=form_values.get("description", ""),
        transaction_date=transaction_date,
    )


def _required_form_value(form_values: dict[str, str], field_name: str, message: str) -> str:
    value = form_values.get(field_name, "").strip()
    if not value:
        raise ValueError(message)
    return value


def _filter_transactions(transactions: list[Transaction], state: PageState) -> list[Transaction]:
    ledger = TransactionLedger(transactions)
    transaction_type = state.selected_type if state.selected_type in {"income", "expense"} else None
    category = state.selected_category if state.selected_category else None
    return list(reversed(ledger.filter_transactions(transaction_type=transaction_type, category=category)))


def _render_transaction_rows(transactions: list[Transaction]) -> str:
    if not transactions:
        return '<div class="empty">Aún no hay movimientos para mostrar con estos filtros.</div>'

    rows: list[str] = []
    for transaction in transactions:
        type_label = "Ingreso" if transaction.is_income else "Gasto"
        amount_class = "income" if transaction.is_income else "expense"
        amount_prefix = "+" if transaction.is_income else "-"
        rows.append(
            "".join(
                [
                    "<tr>",
                    f"<td>{escape(transaction.transaction_date.isoformat())}</td>",
                    f"<td><span class=\"pill\">{type_label}</span></td>",
                    f"<td>{escape(transaction.category)}</td>",
                    f"<td>{escape(transaction.description) or 'Sin descripción'}</td>",
                    f"<td class=\"amount {amount_class}\">{amount_prefix}{_format_money(transaction.amount)}</td>",
                    "</tr>",
                ]
            )
        )

    return (
        '<div class="table-wrap"><table>'
        "<thead><tr><th>Fecha</th><th>Tipo</th><th>Categoría</th><th>Descripción</th><th>Monto</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def _render_category_options(categories: list[str], selected_category: str) -> str:
    return "".join(
        f'<option value="{escape(category, quote=True)}"{_selected(category, selected_category)}>{escape(category)}</option>'
        for category in categories
    )


def _render_type_option(value: str, label: str, selected_value: str) -> str:
    return f'<option value="{escape(value, quote=True)}"{_selected(value, selected_value)}>{escape(label)}</option>'


def _render_notice(message: str, variant: str) -> str:
    return f'<div class="notice {escape(variant, quote=True)}" role="status">{escape(message)}</div>'


def _unique_categories(transactions: list[Transaction]) -> list[str]:
    return sorted({transaction.category for transaction in transactions}, key=str.casefold)


def _first_query_value(query_values: dict[str, list[str]], field_name: str) -> str:
    values = query_values.get(field_name, [""])
    return values[0].strip() if values else ""


def _selected(value: str, selected_value: str) -> str:
    return " selected" if value == selected_value else ""


def _format_money(value: float) -> str:
    return f"S/ {value:,.2f}"


__all__ = [
    "DEFAULT_DATABASE_PATH",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "WebAppConfig",
    "create_server",
    "render_dashboard",
    "serve",
]
