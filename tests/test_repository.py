from __future__ import annotations

from importlib import import_module
import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path
from typing import Any


def load_repository_symbols() -> tuple[Any, Any, Any]:
    domain_module = import_module("expense_control.domain")
    repository_module = import_module("expense_control.repository")

    return (
        domain_module.Transaction,
        domain_module.TransactionType,
        repository_module.SQLiteTransactionRepository,
    )


Transaction: Any
TransactionType: Any
SQLiteTransactionRepository: Any
Transaction, TransactionType, SQLiteTransactionRepository = load_repository_symbols()


class SQLiteTransactionRepositoryTestCase(unittest.TestCase):
    _temporary_directory: tempfile.TemporaryDirectory[str] | None
    database_path: Path
    repository: Any

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._temporary_directory = None
        self.database_path = Path()
        self.repository = None

    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary_directory.cleanup)
        self.database_path = Path(self._temporary_directory.name) / "expense-control-test.sqlite3"
        self.repository = SQLiteTransactionRepository(self.database_path)

    def test_repository_initializes_schema_automatically(self) -> None:
        self.assertTrue(self.database_path.exists())
        self.assertEqual([], self.repository.list_transactions())

        with sqlite3.connect(self.database_path) as connection:
            table_names = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }

        self.assertIn("transactions", table_names)

    def test_repository_saves_and_lists_transactions_as_domain_objects(self) -> None:
        salary = Transaction(
            transaction_type=TransactionType.INCOME,
            amount=3000,
            category="Salary",
            description="Monthly salary",
            transaction_date=date(2026, 6, 1),
        )
        groceries = Transaction(
            transaction_type=TransactionType.EXPENSE,
            amount=120.5,
            category="Food",
            description="Groceries",
            transaction_date=date(2026, 6, 2),
        )

        salary_id = self.repository.save_transaction(salary)
        groceries_id = self.repository.save_transaction(groceries)

        reloaded_repository = SQLiteTransactionRepository(self.database_path)

        self.assertIsInstance(salary_id, int)
        self.assertGreater(salary_id, 0)
        self.assertIsInstance(groceries_id, int)
        self.assertGreater(groceries_id, salary_id)
        self.assertEqual([salary, groceries], reloaded_repository.list_transactions())

    def test_repository_deletes_transactions_by_identifier(self) -> None:
        salary = Transaction(
            transaction_type=TransactionType.INCOME,
            amount=3000,
            category="Salary",
            description="Monthly salary",
            transaction_date=date(2026, 6, 1),
        )
        rent = Transaction(
            transaction_type=TransactionType.EXPENSE,
            amount=900,
            category="Housing",
            description="Rent",
            transaction_date=date(2026, 6, 5),
        )

        salary_id = self.repository.save_transaction(salary)
        rent_id = self.repository.save_transaction(rent)

        self.assertTrue(self.repository.delete_transaction(salary_id))
        self.assertEqual([rent], self.repository.list_transactions())
        self.assertFalse(self.repository.delete_transaction(salary_id))
        self.assertTrue(self.repository.delete_transaction(rent_id))
        self.assertEqual([], self.repository.list_transactions())

    def test_repository_rejects_invalid_transaction_instances(self) -> None:
        with self.assertRaises(TypeError):
            self.repository.save_transaction(object())  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
