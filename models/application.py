"""Сущность отклика на заказ."""

from __future__ import annotations

from typing import Any, Optional

from .order import Order
from .serializable import Serializable
from .user import Executor, User


class Application(Serializable):
    """Отклик исполнителя на заказ."""

    def __init__(
        self,
        application_id: int,
        order: Optional[Order],
        executor: Optional[User],
        comment: str = "",
        order_id: str = "",
        executor_id: str = "",
    ) -> None:
        missing_order = not order_id and order is None
        missing_executor = not executor_id and executor is None
        if missing_order or missing_executor:
            raise ValueError("ID заказа и исполнителя обязательны")
        if executor is not None and not isinstance(executor, Executor):
            raise ValueError("Отклик может создать только исполнитель")
        self.id = application_id
        self.order = order
        self.executor = executor
        self.comment = comment
        self._order_id = str(order.id) if order else str(order_id)
        self._executor_id = str(executor.id) if executor else str(executor_id)

    @property
    def order_id(self) -> str:
        return str(self.order.id) if self.order else self._order_id

    @property
    def executor_id(self) -> str:
        return str(self.executor.id) if self.executor else self._executor_id

    def accept(self) -> None:
        if self.order is None or self.executor is None:
            raise ValueError("Невозможно принять отклик без заказа и исполнителя")
        self.order.assign_executor(self.executor)

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], orders: dict[str, Order], users: dict[str, User]
    ) -> Application:
        order_id = str(data["order_id"])
        executor_id = str(data["executor_id"])
        return cls(
            application_id=int(data["id"]),
            order=orders.get(order_id),
            executor=users.get(executor_id),
            comment=str(data.get("comment", "")),
            order_id=order_id,
            executor_id=executor_id,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
            "comment": self.comment,
        }

    def __str__(self) -> str:
        return (
            f"Отклик #{self.id}: заказ={self.order_id}, "
            f"исполнитель={self.executor_id}"
        )
