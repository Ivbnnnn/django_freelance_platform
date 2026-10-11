from django.shortcuts import render

from homepage.views import detail_page, detail_rows, not_found, object_link, status_badge
from services.transactions import list_transactions


def index(request):
    return render(request, "transactions/transaction_list.html", {"transactions": list_transactions()})


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
