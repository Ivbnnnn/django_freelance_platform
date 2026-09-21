"""Сущность заказа."""

from __future__ import annotations

from typing import Any, Optional

from .serializable import Serializable
from .user import Executor, User


class Order(Serializable):
    """Заказ, опубликованный заказчиком."""

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_PAID = "paid"

    def __init__(
        self,
        order_id: int,
        name: str,
        budget: str,
        customer: Optional[User] = None,
        customer_id: str = "",
        status: str = STATUS_NEW,
    ) -> None:
        if not name or not budget:
            raise ValueError("Название и бюджет обязательны")
        self.id = order_id
        self.name = name
        self.budget = budget
        self.customer = customer
        self._customer_id = str(customer.id) if customer else str(customer_id)
        self.status = status

    @property
    def customer_id(self) -> str:
        return str(self.customer.id) if self.customer else self._customer_id

    def assign_executor(self, executor: User) -> None:
        if not isinstance(executor, Executor):
            raise ValueError("Исполнителем может быть только пользователь с ролью исполнителя")
        self.status = self.STATUS_IN_PROGRESS

    def mark_paid(self) -> None:
        self.status = self.STATUS_PAID

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], users: dict[str, User]
    ) -> Order:
        customer_id = str(data.get("customer_id", ""))
        return cls(
            order_id=int(data["id"]),
            name=str(data["name"]),
            budget=str(data["budget"]),
            customer=users.get(customer_id),
            customer_id=customer_id,
            status=str(data.get("status", cls.STATUS_NEW)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "budget": self.budget,
            "customer_id": self.customer_id,
            "status": self.status,
        }

    def __str__(self) -> str:
        customer = f", заказчик={self.customer_id}" if self.customer_id else ""
        return (
            f"Заказ #{self.id}: {self.name}, бюджет {self.budget}, "
            f"{self.status}{customer}"
        )
