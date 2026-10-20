"""Rebuild the standalone SQLite database from the original JSON files."""

import json
from contextlib import closing
from pathlib import Path

from .database import DATABASE, ROOT, connect

DATA = ROOT / "data"


def records(name):
    with (DATA / name).open(encoding="utf-8") as source:
        return json.load(source)


def existing_id(value, ids):
    """Preserve invalid historical references as source text, with a NULL FK."""
    try:
        number = int(value)
    except (ValueError, TypeError):
        return None
    return number if number in ids else None


def import_data(path=DATABASE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    users = records("users.json")
    orders = records("orders.json")
    applications = records("applications.json")
    transactions = records("transactions.json")
    reviews = records("reviews.json")
    user_ids = {item["id"] for item in users}
    order_ids = {item["id"] for item in orders}
    with closing(connect(path)) as connection, connection:
        connection.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
        for table in ("reviews", "transactions", "applications", "orders", "users"):
            connection.execute(f"DELETE FROM {table}")
        connection.executemany(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
            [(u["id"], u["name"], u["second_name"], u["role"],
              u["password"], u["email"]) for u in users],
        )
        connection.executemany(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
            [(o["id"], o["name"], o["budget"],
              existing_id(o.get("customer_id"), user_ids),
              str(o.get("customer_id", "")), o.get("status", "new"))
             for o in orders],
        )
        connection.executemany(
            "INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?)",
            [(a["id"], existing_id(a["order_id"], order_ids),
              existing_id(a["executor_id"], user_ids),
              str(a["order_id"]), str(a["executor_id"]), a.get("comment", ""))
             for a in applications],
        )
        connection.executemany(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
            [(t["id"], existing_id(t["order_id"], order_ids),
              str(t["order_id"]), str(t["amount"]), t.get("status", "paid"))
             for t in transactions],
        )
        connection.executemany(
            "INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?)",
            [(r["id"], existing_id(r["order_id"], order_ids),
              existing_id(r["author_id"], user_ids), str(r["order_id"]),
              str(r["author_id"]), r["rating"], r.get("text", ""))
             for r in reviews],
        )
        connection.commit()
    return path


if __name__ == "__main__":
    print(import_data())
