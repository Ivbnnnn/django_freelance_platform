from models import Order
from .users import list_users
from .utils import read_data, write_data


def list_orders() -> list[Order]:
    """Загружает заказы и связывает их с объектами заказчиков."""
    users = {str(user.id): user for user in list_users()}
    return [Order.from_dict(record, users) for record in read_data("orders.json")]


def create_order(name: str, budget: str, customer_id: str = "") -> Order:
    orders = list_orders()
    users = {str(user.id): user for user in list_users()}
    order = Order(
        order_id=max((item.id for item in orders), default=0) + 1,
        name=name,
        budget=budget,
        customer=users.get(str(customer_id)),
        customer_id=str(customer_id),
    )
    orders.append(order)
    write_data("orders.json", orders)
    return order
