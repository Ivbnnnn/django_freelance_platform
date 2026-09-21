"""Сущности пользователей сервиса поиска исполнителей."""

from __future__ import annotations

from typing import Any

from .serializable import Serializable


class User(Serializable):
    """Зарегистрированный пользователь сервиса с инкапсулированным паролем."""

    CUSTOMER = "Заказчик"
    EXECUTOR = "Исполнитель"
    VALID_ROLES = (CUSTOMER, EXECUTOR)

    def __init__(
        self,
        user_id: int,
        name: str,
        second_name: str,
        role: str,
        password: str,
        email: str,
    ) -> None:
        if not all((name, second_name, role, password, email)):
            raise ValueError("Все поля пользователя обязательны")
        if role not in self.VALID_ROLES:
            raise ValueError("Некорректная роль")
        self.id = user_id
        self.name = name
        self.second_name = second_name
        self.role = role
        self._password = password
        self.email = email

    @classmethod
    def create(cls, **data: Any) -> User:
        """Создаёт подкласс пользователя по роли из JSON-совместимого словаря."""
        role = data["role"]
        if role not in cls.VALID_ROLES:
            raise ValueError("Некорректная роль")
        user_class = Customer if role == cls.CUSTOMER else Executor
        return user_class(
            user_id=int(data["id"]),
            name=str(data["name"]),
            second_name=str(data["second_name"]),
            password=str(data["password"]),
            email=str(data["email"]),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls.create(**data)

    def check_password(self, password: str) -> bool:
        return self._password == password

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "second_name": self.second_name,
            "role": self.role,
            "password": self._password,
            "email": self.email,
        }

    def __str__(self) -> str:
        return f"{self.role}: {self.name} {self.second_name} (id={self.id})"


class Customer(User):
    """Пользователь, публикующий заказы."""

    def __init__(
        self, user_id: int, name: str, second_name: str, password: str, email: str
    ) -> None:
        super().__init__(user_id, name, second_name, self.CUSTOMER, password, email)


class Executor(User):
    """Пользователь, откликающийся на заказы."""

    def __init__(
        self, user_id: int, name: str, second_name: str, password: str, email: str
    ) -> None:
        super().__init__(user_id, name, second_name, self.EXECUTOR, password, email)
