"""SQL backed records shaped for the existing Django templates."""

from types import SimpleNamespace

from .database import fetch


def _linked(row, prefix, key):
    if row[key] is None:
        return None
    return SimpleNamespace(
        id=row[key], name=row[f"{prefix}_name"],
        second_name=row[f"{prefix}_second_name"] if prefix == "customer" else "",
    )


def _record(kind, row):
    data = dict(row)
    if kind == "users":
        return SimpleNamespace(**data)
    if kind == "orders":
        data["customer"] = _linked(row, "customer", "customer_id")
        data["customer_id"] = row["source_customer_id"]
    elif kind == "applications":
        data["order"] = (SimpleNamespace(id=row["order_id"], name=row["order_name"])
                         if row["order_id"] is not None else None)
        data["executor"] = (SimpleNamespace(id=row["executor_id"],
                                            name=row["executor_name"],
                                            second_name=row["executor_second_name"])
                            if row["executor_id"] is not None else None)
        data["order_id"] = row["source_order_id"]
        data["executor_id"] = row["source_executor_id"]
    elif kind == "transactions":
        data["order"] = (SimpleNamespace(id=row["order_id"], name=row["order_name"])
                         if row["order_id"] is not None else None)
        data["order_id"] = row["source_order_id"]
    elif kind == "reviews":
        data["order"] = (SimpleNamespace(id=row["order_id"], name=row["order_name"])
                         if row["order_id"] is not None else None)
        data["author"] = (SimpleNamespace(id=row["author_id"], name=row["author_name"])
                          if row["author_id"] is not None else None)
        data["order_id"] = row["source_order_id"]
        data["author_id"] = row["source_author_id"]
    return SimpleNamespace(**data)


def list_records(kind):
    return [_record(kind, row) for row in fetch(f"{kind}_list")]


def get_record(kind, identifier):
    rows = fetch(f"{kind[:-1] if kind != 'profiles' else 'user'}_by_id", (identifier,))
    return _record(kind, rows[0]) if rows else None


def search_open_orders(term):
    escaped = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return [_record("orders", row) for row in fetch("open_orders_search", (f"%{escaped}%",))]


def statistics():
    return {
        "orders_count": fetch("orders_count")[0]["total"],
        "applications_count": fetch("applications_count")[0]["total"],
        "orders_by_status": fetch("orders_by_status"),
        "applications_by_order": fetch("applications_by_order"),
        "payments_by_order": fetch("payments_by_order"),
    }
