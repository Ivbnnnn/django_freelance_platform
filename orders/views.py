from django.shortcuts import render

from homepage.views import detail_page, detail_rows, not_found, object_link, status_badge
from services.orders import list_orders


def index(request):
    return render(request, "orders/order_list.html", {"orders": list_orders()})


def detail(request, order_id):
    order = next((item for item in list_orders() if item.id == order_id), None)
    if order is None:
        return not_found("Заказ не найден", "orders:index")

    customer_name = f"{order.customer.name} {order.customer.second_name}" if order.customer else ""
    customer = object_link(order.customer, order.customer_id, "profiles:detail", "user_id", customer_name)
    rows = detail_rows(
        ("ID", order.id),
        ("Название", order.name),
        ("Бюджет", order.budget),
        ("Статус", status_badge(order.status)),
        ("Заказчик", customer),
    )
    return detail_page(f"Заказ №{order.id}", rows, "orders:index")
