from django.core.paginator import Paginator
from django.db.models import Count, F, Q, Sum
from django.shortcuts import get_object_or_404, render

from applications.models import Application
from .forms import OrderFilterForm
from .models import Order


def index(request):
    form = OrderFilterForm(request.GET)
    orders = Order.objects.with_customer()
    if form.is_valid():
        data = form.cleaned_data
        if data['q']:
            orders = orders.search(data['q'])
        if data['status']:
            orders = orders.filter(status=data['status'])
        if data['customer']:
            orders = orders.filter(customer=data['customer'])
        sorts = {'id': ('id',), '-id': ('-id',), 'name': ('name', 'id'),
                 'customer': ('customer__name', 'customer__second_name', 'id')}
        orders = orders.order_by(*sorts.get(data['sort'], ('id',)))
    else:
        orders = orders.none()
    page = Paginator(orders, 5).get_page(request.GET.get('page'))
    return render(request, 'orders/order_list.html', {'orders': page.object_list, 'page_obj': page, 'form': form})


def detail(request, order_id):
    order = get_object_or_404(
        Order.objects.with_customer().prefetch_related('applications__executor'), pk=order_id,
    )
    return render(request, 'orders/order_detail.html', {'order': order})


def search(request):
    query = request.GET.get('q', '').strip()[:100]
    orders = Order.objects.available()
    orders = orders.filter(name__icontains=query).select_related('customer').order_by('name', 'id')
    return render(request, 'orders/search.html', {'query': query, 'orders': orders})


def stats(request):
    totals = Order.objects.aggregate(
        orders_count=Count('id'), open_count=Count('id', filter=Q(status=Order.Status.NEW)),
    )
    return render(request, 'orders/statistics.html', {
        **totals,
        'applications_count': Application.objects.count(),
        'active_count': Order.objects.active().count(),
        'orders_by_status': Order.objects.values('status').annotate(total=Count('id')).order_by('status'),
        'applications_by_order': Order.objects.annotate(total=Count('applications')).values('id', 'name', 'total'),
        'payments_by_order': Order.objects.annotate(
            payment_count=Count('transactions', filter=Q(transactions__status='paid')),
            amount_total=Sum('transactions__amount', filter=Q(transactions__status='paid'), default=0),
        ).values('id', 'name', 'payment_count', 'amount_total'),
        'customer_totals': Order.objects.annotate(customer_name=F('customer__name')).values('customer_name')
        .annotate(total=Count('id')).order_by('-total', 'customer_name'),
    })
