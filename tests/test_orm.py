from decimal import Decimal
from io import StringIO

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command, CommandError
from django.db.models.deletion import ProtectedError
from django.test import Client

from applications.models import Application
from orders.models import Order
from profiles.models import User
from reviews.models import Review
from transactions.models import Transaction

pytestmark = pytest.mark.django_db


def test_crud_relations_and_protected_deletion():
    user = User.objects.create(name='Анна', role='Заказчик')
    order = Order.objects.create(name='Дизайн', budget='1000-2000', customer=user)
    application = Application.objects.create(order=order, executor=user)
    assert list(user.orders.all()) == [order]
    assert application.order.customer == user
    order.name = 'Логотип'
    order.save()
    assert Order.objects.get(pk=order.pk).name == 'Логотип'
    assert order.get_absolute_url() == f'/orders/{order.pk}/'
    with pytest.raises(ProtectedError):
        order.delete()
    application.delete()
    order.delete()
    assert not Order.objects.exists()


def test_validation():
    with pytest.raises(ValidationError):
        Review(rating=6).full_clean()
    with pytest.raises(ValidationError):
        Transaction(amount=Decimal('-1')).full_clean()
    with pytest.raises(ValidationError):
        Order(name='Заказ', budget='1', status='wrong').full_clean()


def test_filters_sort_and_pagination():
    user = User.objects.create(name='Анна', role='Заказчик')
    other = User.objects.create(name='Борис', role='Заказчик')
    for i in range(12):
        Order.objects.create(name=f'Заказ {i:02}', budget='100', customer=user)
    Order.objects.create(name='Скрытый', budget='100', customer=other, status=Order.Status.CANCELLED)
    client = Client()
    params = {'q': 'Анна', 'status': 'new', 'customer': user.pk, 'sort': '-id', 'page': '2'}
    response = client.get('/orders/', params)
    page = response.context['page_obj']
    assert page.paginator.count == 12
    assert [o.pk for o in page.object_list] == list(range(7, 2, -1))
    assert 'status=new' in response.content.decode()
    assert 'sort=-id' in response.content.decode()
    assert 'page=3' in response.content.decode()
    assert 'Скрытый' not in client.get('/orders/search/').content.decode()
    for params in [{'customer': 'oops'}, {'status': 'oops'}, {'sort': 'password'}, {'page_size': '100000'}]:
        response = client.get('/orders/', params)
        assert response.status_code == 200
        assert response.context['form'].errors
        assert response.context['page_obj'].paginator.count == 0
    assert client.get('/orders/', {'page_size': '1'}).context['page_obj'].paginator.num_pages == 13
    assert client.get('/orders/', {'page': 'oops'}).context['page_obj'].number == 1
    assert client.get('/orders/', {'page': '999'}).context['page_obj'].number == 3


def test_statistics_do_not_multiply_joins_and_ignore_cancelled_payments():
    order = Order.objects.create(name='Логотип', budget='100')
    for _ in range(3):
        Application.objects.create(order=order)
    Transaction.objects.create(order=order, amount=Decimal('10.50'), status='paid')
    Transaction.objects.create(order=order, amount=Decimal('20'), status='paid')
    Transaction.objects.create(order=order, amount=Decimal('999'), status='cancelled')
    Order.objects.create(name='Пустой', budget='0')
    context = Client().get('/orders/statistics/').context
    payments = list(context['payments_by_order'])
    assert payments[0]['payment_count'] == 2
    assert payments[0]['amount_total'] == Decimal('30.50')
    assert payments[1]['payment_count'] == 0
    assert list(context['applications_by_order'])[0]['total'] == 3
    assert context['open_count'] == 2


def test_empty_pages_and_no_fallback_to_legacy():
    client = Client()
    for url in ['/orders/', '/applications/', '/transactions/', '/reviews/', '/profiles/',
                '/orders/statistics/', '/orders/search/']:
        assert client.get(url).status_code == 200
    assert client.get('/orders/1/').status_code == 404


def test_import_refuses_nonempty_database_without_changes():
    User.objects.create(name='Сохранён', role='Заказчик')
    with pytest.raises(CommandError, match='не пусты'):
        call_command('import_legacy', stdout=StringIO())
    assert User.objects.get().name == 'Сохранён'
