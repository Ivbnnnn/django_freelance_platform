import json
from pathlib import Path
from typing import Any, Iterable

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_data(name: str) -> list[dict[str, Any]]:
    """Читает исходные записи JSON из файла данных.

    Преобразование записей в объекты выполняет соответствующий сервис, потому
    что только он знает, как восстановить связи между объектами.
    """
    path = DATA_DIR / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _serialize(item: Any) -> Any:
    return item.to_dict() if hasattr(item, "to_dict") else item


def write_data(name: str, data: Iterable[Any]) -> list[Any]:
    """Сохраняет словари или сериализуемые объекты предметной области в JSON."""
    records = [_serialize(item) for item in data]
    DATA_DIR.mkdir(exist_ok=True)
    with (DATA_DIR / name).open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)
    return records


def append_data(name: str, item: dict[str, Any]) -> dict[str, Any]:
    """Совместимый вспомогательный метод для записей предыдущей версии."""
    items = read_data(name)
    next_id = max((int(record.get("id", 0)) for record in items), default=0) + 1
    item = {"id": next_id, **item}
    items.append(item)
    write_data(name, items)
    return item
