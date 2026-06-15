from __future__ import annotations

import os
from pathlib import Path

from .web import DEFAULT_HOST, DEFAULT_PORT, WebAppConfig, serve


def main() -> None:
    host = os.environ.get("EXPENSE_CONTROL_HOST", DEFAULT_HOST)
    port = int(os.environ.get("EXPENSE_CONTROL_PORT", str(DEFAULT_PORT)))
    database_path = Path(os.environ.get("EXPENSE_CONTROL_DB", "data/expense-control.sqlite3"))

    serve(WebAppConfig(host=host, port=port, database_path=database_path))


if __name__ == "__main__":
    main()
