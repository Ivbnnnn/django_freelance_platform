"""Базовый класс для объектов, сохраняемых в JSON."""

from typing import Any


class Serializable:
    """Базовый класс сущностей предметной области, сохраняемых в JSON."""

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError

    def __getitem__(self, key: str) -> Any:
        """Сохраняет доступ по ключу, использовавшийся в прежней модели словарей."""
        return self.to_dict()[key]
