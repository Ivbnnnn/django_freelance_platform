from django.shortcuts import render

from services.orders import list_orders


def index(request):
    return render(request, "orders/order_list.html", {"orders": list_orders()})


def detail(request, order_id):
    order = next((item for item in list_orders() if item.id == order_id), None)
    if order is None:
        return render(request, "record_not_found.html", {
            "title": "Заказ не найден", "back_route": "orders:index",
        }, status=404)
    return render(request, "orders/order_detail.html", {"order": order})
