from django.urls import reverse
from django.utils.html import format_html_join

from homepage.views import detail_page, detail_rows, list_page, not_found, object_link, status_badge
from services.transactions import list_transactions


def index(request):
    items = format_html_join(
        "",
        '<a class="list-group-item list-group-item-action d-flex justify-content-between gap-3" href="{}">'
        '<span><strong>Платёж №{}</strong> · Заказ №{} · {}</span>{}</a>',
        (
            (reverse("transactions:detail", kwargs={"transaction_id": item.id}), item.id, item.order_id,
             item.amount, status_badge(item.status))
            for item in list_transactions()
        ),
    )
    return list_page("Платежи", "Операции оплаты по заказам.", items)


def detail(request, transaction_id):
    transaction = next((item for item in list_transactions() if item.id == transaction_id), None)
    if transaction is None:
        return not_found("Платёж не найден", "transactions:index")

    order_name = transaction.order.name if transaction.order else ""
    rows = detail_rows(
        ("ID", transaction.id),
        ("Заказ", object_link(transaction.order, transaction.order_id, "orders:detail", "order_id", order_name)),
        ("Сумма", transaction.amount),
        ("Статус", status_badge(transaction.status)),
    )
    return detail_page(f"Платёж №{transaction.id}", rows, "transactions:index")
