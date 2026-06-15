from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path
from typing import Any


def load_domain_symbols() -> tuple[Any, Any, Any]:
    module_path = Path(__file__).resolve().parents[1] / "src" / "expense_control" / "domain.py"
    spec = importlib.util.spec_from_file_location("expense_control.domain", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load domain module from {module_path}")

    domain_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = domain_module
    spec.loader.exec_module(domain_module)

    return (
        domain_module.Transaction,
        domain_module.TransactionLedger,
        domain_module.TransactionType,
    )


Transaction: Any
TransactionLedger: Any
TransactionType: Any
Transaction, TransactionLedger, TransactionType = load_domain_symbols()


def build_sample_ledger() -> tuple[Any, Any, Any, Any, Any]:
    salary = Transaction(
        transaction_type=TransactionType.INCOME,
        amount=3000,
        category="Salary",
        description="Monthly salary",
        transaction_date=date(2026, 6, 1),
    )
    freelance = Transaction(
        transaction_type=TransactionType.INCOME,
        amount=450,
        category="Freelance",
        description="Side project",
        transaction_date=date(2026, 6, 10),
    )
    rent = Transaction(
        transaction_type=TransactionType.EXPENSE,
        amount=900,
        category="Housing",
        description="Rent",
        transaction_date=date(2026, 6, 5),
    )
    groceries = Transaction(
        transaction_type=TransactionType.EXPENSE,
        amount=120.5,
        category="Food",
        description="Groceries",
        transaction_date=date(2026, 6, 12),
    )
    ledger = TransactionLedger([salary, freelance, rent, groceries])

    return ledger, salary, freelance, rent, groceries


class TransactionTestCase(unittest.TestCase):
    def test_transaction_normalizes_and_preserves_expected_fields(self) -> None:
        transaction = Transaction(
            transaction_type=" income ",
            amount=1250,
            category=" Salary ",
            description=" June payment ",
            transaction_date=date(2026, 6, 1),
        )

        self.assertEqual(TransactionType.INCOME, transaction.transaction_type)
        self.assertEqual(1250.0, transaction.amount)
        self.assertEqual("Salary", transaction.category)
        self.assertEqual("June payment", transaction.description)
        self.assertEqual(date(2026, 6, 1), transaction.transaction_date)
        self.assertTrue(transaction.is_income)
        self.assertFalse(transaction.is_expense)

    def test_transaction_rejects_zero_or_negative_amounts(self) -> None:
        for invalid_amount in (0, -1, -15.75):
            with self.subTest(amount=invalid_amount):
                with self.assertRaises(ValueError):
                    Transaction(
                        transaction_type=TransactionType.EXPENSE,
                        amount=invalid_amount,
                        category="Food",
                        description="Lunch",
                        transaction_date=date(2026, 6, 2),
                    )

    def test_transaction_rejects_invalid_type(self) -> None:
        with self.assertRaises(ValueError):
            Transaction(
                transaction_type="transfer",
                amount=100,
                category="Other",
                description="Invalid type",
                transaction_date=date(2026, 6, 3),
            )


class TransactionLedgerTestCase(unittest.TestCase):
    def test_ledger_calculates_income_expenses_and_balance(self) -> None:
        ledger, _, _, _, _ = build_sample_ledger()

        self.assertEqual(3450.0, ledger.total_income())
        self.assertEqual(1020.5, ledger.total_expenses())
        self.assertEqual(2429.5, ledger.balance())

    def test_ledger_filters_by_transaction_type(self) -> None:
        ledger, _, _, rent, groceries = build_sample_ledger()

        expenses = ledger.filter_transactions(transaction_type="expense")

        self.assertEqual([rent, groceries], expenses)

    def test_ledger_filters_by_category(self) -> None:
        ledger, salary, _, _, _ = build_sample_ledger()

        salary_transactions = ledger.filter_transactions(category=" Salary ")

        self.assertEqual([salary], salary_transactions)

    def test_ledger_filters_by_inclusive_date_range(self) -> None:
        ledger, _, freelance, rent, _ = build_sample_ledger()

        june_window = ledger.filter_transactions(
            start_date=date(2026, 6, 5),
            end_date=date(2026, 6, 10),
        )

        self.assertEqual([rent, freelance], june_window)

    def test_ledger_combines_filters(self) -> None:
        ledger, _, _, _, groceries = build_sample_ledger()

        filtered_transactions = ledger.filter_transactions(
            transaction_type=TransactionType.EXPENSE,
            category="Food",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 30),
        )

        self.assertEqual([groceries], filtered_transactions)

    def test_ledger_rejects_invalid_date_range(self) -> None:
        ledger, _, _, _, _ = build_sample_ledger()

        with self.assertRaises(ValueError):
            ledger.filter_transactions(
                start_date=date(2026, 6, 30),
                end_date=date(2026, 6, 1),
            )
