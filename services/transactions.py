from models import Transaction
from .orders import list_orders
from .utils import read_data, write_data


def list_transactions() -> list[Transaction]:
    orders = {str(order.id): order for order in list_orders()}
    return [
        Transaction.from_dict(record, orders)
        for record in read_data("transactions.json")
    ]


def create_transaction(order_id: str, amount: str) -> Transaction:
    transactions = list_transactions()
    orders = list_orders()
    order_index = {str(order.id): order for order in orders}
    transaction = Transaction(
        transaction_id=max((item.id for item in transactions), default=0) + 1,
        order=order_index.get(str(order_id)),
        amount=amount,
        order_id=str(order_id),
    )
    transaction.pay()
    transactions.append(transaction)
    write_data("transactions.json", transactions)
    if transaction.order is not None:
        write_data("orders.json", orders)
    return transaction
