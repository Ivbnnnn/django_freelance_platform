from .utils import append_data, read_data
def create_transaction(order_id, amount): return append_data("transactions.json", {"order_id": order_id, "amount": amount, "status": "paid"})
def list_transactions(): return read_data("transactions.json")
