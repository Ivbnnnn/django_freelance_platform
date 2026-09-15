from .utils import append_data, read_data


def create_application(order_id, executor_id, comment=""):
    if not order_id or not executor_id:
        raise ValueError("ID обязательны")
    return append_data(
        "applications.json",
        {"order_id": order_id, "executor_id": executor_id, "comment": comment},
    )


def list_applications():
    return read_data("applications.json")
