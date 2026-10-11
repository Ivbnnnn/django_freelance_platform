from django.shortcuts import render

from services.transactions import list_transactions


def index(request):
    return render(request, "transactions/transaction_list.html", {"transactions": list_transactions()})


def detail(request, transaction_id):
    transaction = next((item for item in list_transactions() if item.id == transaction_id), None)
    if transaction is None:
        return render(request, "record_not_found.html", {
            "title": "Платёж не найден", "back_route": "transactions:index",
        }, status=404)
    return render(request, "transactions/transaction_detail.html", {"transaction": transaction})
