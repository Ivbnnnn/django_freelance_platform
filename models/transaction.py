"""Сущность платёжной транзакции."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Optional

from .order import Order
from .serializable import Serializable


class Transaction(Serializable):
    """Платёж по заказу."""

    def __init__(
        self,
        transaction_id: int,
        order: Optional[Order],
        amount: str,
        status: str = "paid",
        order_id: str = "",
    ) -> None:
        try:
            if Decimal(str(amount)) <= 0:
                raise ValueError
        except (InvalidOperation, ValueError) as error:
            raise ValueError("Сумма должна быть положительным числом") from error
        self.id = transaction_id
        self.order = order
        self.amount = str(amount)
        self.status = status
        self._order_id = str(order.id) if order else str(order_id)

    @property
    def order_id(self) -> str:
        return str(self.order.id) if self.order else self._order_id

    def pay(self) -> None:
        self.status = "paid"
        if self.order is not None:
            self.order.mark_paid()

    @classmethod
    def from_dict(cls, data: dict[str, Any], orders: dict[str, Order]) -> Transaction:
        order_id = str(data["order_id"])
        return cls(
            transaction_id=int(data["id"]),
            order=orders.get(order_id),
            amount=str(data["amount"]),
            status=str(data.get("status", "paid")),
            order_id=order_id,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "amount": self.amount,
            "status": self.status,
        }

    def __str__(self) -> str:
        return (
            f"Платёж #{self.id}: заказ={self.order_id}, сумма={self.amount}, "
            f"{self.status}"
        )
