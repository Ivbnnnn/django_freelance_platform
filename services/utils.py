import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_data(name):
    path = DATA_DIR / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def write_data(name, data):
    DATA_DIR.mkdir(exist_ok=True)
    with (DATA_DIR / name).open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return data


def append_data(name, item):
    items = read_data(name)
    item = {"id": len(items) + 1, **item}
    items.append(item)
    write_data(name, items)
    return item
