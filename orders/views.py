from django.http import HttpResponse


def index(request):
    return HttpResponse("Заказы")


def detail(request, order_id):
    return HttpResponse(f"Заказ №{order_id}")
