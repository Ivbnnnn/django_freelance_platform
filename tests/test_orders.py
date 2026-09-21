import pytest

from models import Order
from services.orders import create_order, list_orders


def test_create_order_links_customer(customer):
    order = create_order("Сайт", "10000", str(customer.id))

    assert isinstance(order, Order)
    assert order.customer.id == customer.id
    assert order.customer_id == str(customer.id)
    assert order.status == Order.STATUS_NEW


def test_list_orders_loads_objects(order):
    loaded = list_orders()

    assert isinstance(loaded[0], Order)
    assert loaded[0].to_dict() == order.to_dict()


def test_order_methods_and_serialization(order, executor, customer):
    order.assign_executor(executor)
    order.mark_paid()
    restored = Order.from_dict(order.to_dict(), {str(customer.id): customer})

    assert order.status == Order.STATUS_PAID
    assert restored.customer is customer
    assert "Логотип" in str(restored)


def test_order_rejects_invalid_data(customer):
    with pytest.raises(ValueError):
        create_order("", "100", str(customer.id))

    order = Order(1, "Сайт", "100")
    with pytest.raises(ValueError):
        order.assign_executor(customer)
