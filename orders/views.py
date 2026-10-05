from django.urls import reverse
from django.utils.html import format_html_join

from homepage.views import detail_page, detail_rows, list_page, not_found, object_link, status_badge
from services.orders import list_orders


def index(request):
    items = format_html_join(
        "",
        '<a class="list-group-item list-group-item-action d-flex justify-content-between gap-3" href="{}">'
        '<span><strong>{}</strong><br><small class="text-muted">Бюджет: {}</small></span>{}</a>',
        (
            (reverse("orders:detail", kwargs={"order_id": order.id}), order.name, order.budget, status_badge(order.status))
            for order in list_orders()
        ),
    )
    return list_page("Заказы", "Предложения заказчиков и их текущий статус.", items)


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
