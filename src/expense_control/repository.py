from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path
from typing import cast

from .domain import Transaction, TransactionType


class SQLiteTransactionRepository:
    _database_path: Path

    def __init__(self, database_path: str | Path) -> None:
        self._database_path = Path(database_path)
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def save_transaction(self, transaction: object) -> int:
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction instance")

        transaction_type = TransactionType.from_value(transaction.transaction_type)

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO transactions (
                    transaction_type,
                    amount,
                    category,
                    description,
                    transaction_date
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    transaction_type.value,
                    transaction.amount,
                    transaction.category,
                    transaction.description,
                    transaction.transaction_date.isoformat(),
                ),
            )
            if cursor.lastrowid is None:
                raise RuntimeError("unable to determine inserted transaction id")

            return int(cursor.lastrowid)

    def list_transactions(self) -> list[Transaction]:
        with self._connect() as connection:
            rows: list[sqlite3.Row] = connection.execute(
                """
                SELECT transaction_type, amount, category, description, transaction_date
                FROM transactions
                ORDER BY transaction_date ASC, id ASC
                """
            ).fetchall()

        transactions: list[Transaction] = []
        for row in rows:
            transactions.append(
                Transaction(
                    transaction_type=cast(str, row["transaction_type"]),
                    amount=cast(float, row["amount"]),
                    category=cast(str, row["category"]),
                    description=cast(str, row["description"]),
                    transaction_date=date.fromisoformat(cast(str, row["transaction_date"])),
                )
            )
        return transactions

    def delete_transaction(self, transaction_id: object) -> bool:
        if not isinstance(transaction_id, int) or isinstance(transaction_id, bool):
            raise TypeError("transaction_id must be an integer")

        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM transactions WHERE id = ?",
                (transaction_id,),
            )
            return cursor.rowcount > 0

    def _initialize_schema(self) -> None:
        with self._connect() as connection:
            _ = connection.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('income', 'expense')),
                    amount REAL NOT NULL CHECK (amount > 0),
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    transaction_date TEXT NOT NULL
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        return connection


__all__ = ["SQLiteTransactionRepository"]
