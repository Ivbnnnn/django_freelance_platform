from contextlib import closing

from django.shortcuts import render

from db.database import connect
from db.repository import _record


def index(request):
    with closing(connect()) as conn:
        rows = conn.execute("""
            SELECT t.*, o.name AS order_name
            FROM transactions AS t
            LEFT JOIN orders AS o ON o.id = t.order_id
            ORDER BY t.id;
        """).fetchall()
    return render(request, "transactions/transaction_list.html", {
        "transactions": [_record("transactions", row) for row in rows],
    })


def detail(request, transaction_id):
    with closing(connect()) as conn:
        row = conn.execute("""
            SELECT t.*, o.name AS order_name
            FROM transactions AS t
            LEFT JOIN orders AS o ON o.id = t.order_id
            WHERE t.id = ?;
        """, (transaction_id,)).fetchone()
    if row is None:
        return render(request, "record_not_found.html", {
            "title": "Платёж не найден", "back_route": "transactions:index",
        }, status=404)
    transaction = _record("transactions", row)
    return render(request, "transactions/transaction_detail.html", {"transaction": transaction})
