from orders.models import Order


def site_info(request):
    return {'site_name': 'Сервис поиска исполнителей', 'available_orders_count': Order.objects.available().count()}
