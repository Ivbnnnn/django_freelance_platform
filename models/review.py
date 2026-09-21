"""Сущность отзыва."""

from __future__ import annotations

from typing import Any, Optional

from .order import Order
from .serializable import Serializable
from .user import User


class Review(Serializable):
    """Отзыв, оставленный пользователем о выполненном заказе."""

    def __init__(
        self,
        review_id: int,
        order: Optional[Order],
        author: Optional[User],
        rating: int,
        text: str,
        order_id: str = "",
        author_id: str = "",
    ) -> None:
        if not 1 <= int(rating) <= 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        self.id = review_id
        self.order = order
        self.author = author
        self.rating = int(rating)
        self.text = text
        self._order_id = str(order.id) if order else str(order_id)
        self._author_id = str(author.id) if author else str(author_id)

    @property
    def order_id(self) -> str:
        return str(self.order.id) if self.order else self._order_id

    @property
    def author_id(self) -> str:
        return str(self.author.id) if self.author else self._author_id

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], orders: dict[str, Order], users: dict[str, User]
    ) -> Review:
        order_id = str(data["order_id"])
        author_id = str(data["author_id"])
        return cls(
            review_id=int(data["id"]),
            order=orders.get(order_id),
            author=users.get(author_id),
            rating=int(data["rating"]),
            text=str(data.get("text", "")),
            order_id=order_id,
            author_id=author_id,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "author_id": self.author_id,
            "rating": self.rating,
            "text": self.text,
        }

    def __str__(self) -> str:
        return f"Отзыв #{self.id}: заказ={self.order_id}, оценка={self.rating}/5"
