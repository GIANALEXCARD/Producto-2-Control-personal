from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from numbers import Real


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

    @classmethod
    def from_value(cls, value: object) -> "TransactionType":
        if isinstance(value, cls):
            return value

        if not isinstance(value, str):
            raise TypeError("transaction_type must be a string or TransactionType")

        normalized_value = value.strip().lower()

        try:
            return cls(normalized_value)
        except ValueError as error:
            raise ValueError("transaction_type must be 'income' or 'expense'") from error


def _validate_amount(amount: object) -> float:
    if isinstance(amount, bool) or not isinstance(amount, Real):
        raise TypeError("amount must be a real number")

    normalized_amount = float(amount)
    if normalized_amount <= 0:
        raise ValueError("amount must be greater than zero")

    return normalized_amount


def _normalize_required_text(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name} must not be empty")

    return normalized_value


def _normalize_optional_text(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    return value.strip()


def _validate_transaction_date(transaction_date: object) -> date:
    if not isinstance(transaction_date, date):
        raise TypeError("transaction_date must be a date instance")

    return transaction_date


def _validate_date_range(start_date: date | None, end_date: date | None) -> None:
    if start_date is not None:
        _ = _validate_transaction_date(start_date)
    if end_date is not None:
        _ = _validate_transaction_date(end_date)

    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError("start_date must be earlier than or equal to end_date")


@dataclass(frozen=True, slots=True)
class Transaction:
    transaction_type: TransactionType | str
    amount: float
    category: str
    description: str
    transaction_date: date

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "transaction_type",
            TransactionType.from_value(self.transaction_type),
        )
        object.__setattr__(self, "amount", _validate_amount(self.amount))
        object.__setattr__(self, "category", _normalize_required_text(self.category, "category"))
        object.__setattr__(
            self,
            "description",
            _normalize_optional_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "transaction_date",
            _validate_transaction_date(self.transaction_date),
        )

    @property
    def is_income(self) -> bool:
        return self.transaction_type is TransactionType.INCOME

    @property
    def is_expense(self) -> bool:
        return self.transaction_type is TransactionType.EXPENSE


@dataclass(slots=True)
class TransactionLedger:
    transactions: list[Transaction] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.transactions = list(self.transactions)

    def add_transaction(self, transaction: object) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction instance")

        self.transactions.append(transaction)

    def total_income(self) -> float:
        return sum(transaction.amount for transaction in self.transactions if transaction.is_income)

    def total_expenses(self) -> float:
        return sum(transaction.amount for transaction in self.transactions if transaction.is_expense)

    def balance(self) -> float:
        return self.total_income() - self.total_expenses()

    def filter_transactions(
        self,
        *,
        transaction_type: TransactionType | str | None = None,
        category: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Transaction]:
        normalized_type = None
        if transaction_type is not None:
            normalized_type = TransactionType.from_value(transaction_type)

        normalized_category = None
        if category is not None:
            normalized_category = _normalize_required_text(category, "category")

        _validate_date_range(start_date, end_date)

        filtered_transactions: list[Transaction] = []
        for transaction in self.transactions:
            if normalized_type is not None and transaction.transaction_type is not normalized_type:
                continue
            if normalized_category is not None and transaction.category != normalized_category:
                continue
            if start_date is not None and transaction.transaction_date < start_date:
                continue
            if end_date is not None and transaction.transaction_date > end_date:
                continue
            filtered_transactions.append(transaction)

        return sorted(filtered_transactions, key=lambda transaction: transaction.transaction_date)


__all__ = ["Transaction", "TransactionLedger", "TransactionType"]
