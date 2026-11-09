from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext

from applications.models import Application
from orders.models import Order
from profiles.models import User

pytestmark = pytest.mark.django_db


def test_availability_changes_with_status():
    order = Order.objects.create(name='Заказ', budget='100')
    assert list(Order.objects.available()) == [order]
    for status in [Order.Status.IN_PROGRESS, Order.Status.CANCELLED, Order.Status.PAID, Order.Status.COMPLETED]:
        order.status = status
        order.save()
        assert not Order.objects.available().exists()
        assert Order.objects.active().exists() == (status == Order.Status.IN_PROGRESS)
    order.status = Order.Status.NEW
    order.save()
    assert Order.objects.available().exists()


def test_admin_access_search_inline_and_edit():
    user = User.objects.create(name='Анна', role='Заказчик')
    order = Order.objects.create(name='Логотип', budget='100', customer=user)
    Application.objects.create(order=order, executor=user, comment='Готов')
    client = Client()
    assert client.get('/admin/orders/order/').status_code == 302
    admin = get_user_model().objects.create_superuser('test-admin', password='test-password')
    client.force_login(admin)
    for app, model in [('orders', 'order'), ('profiles', 'user'), ('applications', 'application'),
                       ('transactions', 'transaction'), ('reviews', 'review')]:
        assert client.get(f'/admin/{app}/{model}/').status_code == 200
    response = client.get('/admin/orders/order/', {'q': 'Анна', 'status__exact': 'new'})
    assert list(response.context['cl'].queryset) == [order]
    assert b'private-secret' not in client.get(f'/admin/profiles/user/{user.pk}/change/').content
    response = client.get(f'/admin/orders/order/{order.pk}/change/')
    assert len(response.context['inline_admin_formsets']) == 3
    # TransactionAdmin actually persists changes and the page sees the ORM update.
    response = client.post('/admin/transactions/transaction/add/', {
        'order': order.pk, 'amount': '12.50', 'status': 'paid', '_save': 'Сохранить',
    })
    assert response.status_code == 302
    assert order.transactions.get().amount == Decimal('12.50')
    assert '12,50' in client.get('/transactions/').content.decode()


def test_related_queries_remain_constant():
    user = User.objects.create(name='Анна', role='Заказчик')
    order = Order.objects.create(name='Логотип', budget='100', customer=user)
    for _ in range(8):
        Application.objects.create(order=order, executor=user)
    with CaptureQueriesContext(connection) as queries:
        record = Order.objects.with_customer().prefetch_related('applications__executor').get(pk=order.pk)
        assert record.customer.name == 'Анна'
        assert [a.executor.name for a in record.applications.all()] == ['Анна'] * 8
    assert len(queries) == 3
    assert 'JOIN' in queries[0]['sql']


def test_context_and_related_values_refresh():
    user = User.objects.create(name='Анна', role='Заказчик')
    order = Order.objects.create(name='Логотип', budget='100', customer=user)
    client = Client()
    assert client.get('/').context['available_orders_count'] == 1
    user.name = 'Анна Новая'
    user.save()
    assert 'Анна Новая' in client.get(order.get_absolute_url()).content.decode()
