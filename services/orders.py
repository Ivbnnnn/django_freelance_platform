from .utils import append_data, read_data


def create_order(name, budget, customer_id=""):
    if not name or not budget:
        raise ValueError("Название и бюджет обязательны")
    return append_data(
        "orders.json",
        {"name": name, "budget": budget, "customer_id": customer_id, "status": "new"},
    )


def list_orders():
    return read_data("orders.json")
