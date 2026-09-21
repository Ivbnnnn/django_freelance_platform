import pytest

from models import Transaction
from services.orders import list_orders
from services.transactions import create_transaction, list_transactions


def test_create_transaction_marks_order_paid(order):
    transaction = create_transaction(str(order.id), "5000")

    assert isinstance(transaction, Transaction)
    assert transaction.status == "paid"
    assert list_orders()[0].status == "paid"


def test_list_transactions_loads_objects(order):
    create_transaction(str(order.id), "5000")

    assert isinstance(list_transactions()[0], Transaction)


def test_transaction_pay_and_serialization(order):
    transaction = Transaction(1, order, "99", status="new")
    transaction.pay()
    restored = Transaction.from_dict(transaction.to_dict(), {str(order.id): order})

    assert restored.order is order
    assert restored["amount"] == "99"
    assert "Платёж" in str(restored)


@pytest.mark.parametrize("amount", ("0", "-1", "не число"))
def test_transaction_rejects_non_positive_amount(amount):
    with pytest.raises(ValueError):
        Transaction(1, None, amount, order_id="1")
