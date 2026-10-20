from django.shortcuts import render
from contextlib import closing

from db.database import connect
from db.repository import _record


def index(request):
    with closing(connect()) as conn:
        rows = conn.execute("""
            SELECT o.*, u.name AS customer_name,
                   u.second_name AS customer_second_name
            FROM orders AS o
            LEFT JOIN users AS u ON u.id = o.customer_id
            ORDER BY o.id;
        """).fetchall()
    orders = [_record("orders", row) for row in rows]
    return render(request, "orders/order_list.html", {"orders": orders})


def detail(request, order_id):
    with closing(connect()) as conn:
        row = conn.execute("""
            SELECT o.*, u.name AS customer_name,
                   u.second_name AS customer_second_name
            FROM orders AS o
            LEFT JOIN users AS u ON u.id = o.customer_id
            WHERE o.id = ?;
        """, (order_id,)).fetchone()
    if row is None:
        return render(request, "record_not_found.html", {
            "title": "Заказ не найден", "back_route": "orders:index",
        }, status=404)
    order = _record("orders", row)
    return render(request, "orders/order_detail.html", {"order": order})


def search(request):
    query = request.GET.get("q", "").strip()
    escaped = query.replace("!", "!!").replace("%", "!%").replace("_", "!_")
    with closing(connect()) as conn:
        rows = conn.execute("""
            SELECT o.*, u.name AS customer_name,
                   u.second_name AS customer_second_name
            FROM orders AS o
            LEFT JOIN users AS u ON u.id = o.customer_id
            WHERE o.status = 'new' AND o.name LIKE ? ESCAPE '!'
            ORDER BY o.id;
        """, (f"%{escaped}%",)).fetchall()
    orders = [_record("orders", row) for row in rows]
    return render(request, "orders/search.html", {
        "query": query, "orders": orders,
    })


def stats(request):
    with closing(connect()) as conn:
        orders_count = conn.execute(
            "SELECT COUNT(*) AS total FROM orders;"
        ).fetchone()["total"]
        applications_count = conn.execute(
            "SELECT COUNT(*) AS total FROM applications;"
        ).fetchone()["total"]
        orders_by_status = conn.execute("""
            SELECT status, COUNT(*) AS total
            FROM orders GROUP BY status ORDER BY status;
        """).fetchall()
        applications_by_order = conn.execute("""
            SELECT o.id, o.name, COUNT(a.id) AS total
            FROM orders AS o
            LEFT JOIN applications AS a ON a.order_id = o.id
            GROUP BY o.id, o.name ORDER BY o.id;
        """).fetchall()
        payments_by_order = conn.execute("""
            SELECT o.id, o.name, COUNT(t.id) AS payment_count,
                   COALESCE(SUM(CAST(t.amount AS REAL)), 0) AS amount_total
            FROM orders AS o
            LEFT JOIN transactions AS t ON t.order_id = o.id
            GROUP BY o.id, o.name ORDER BY o.id;
        """).fetchall()
    return render(request, "orders/statistics.html", {
        "orders_count": orders_count,
        "applications_count": applications_count,
        "orders_by_status": orders_by_status,
        "applications_by_order": applications_by_order,
        "payments_by_order": payments_by_order,
    })
