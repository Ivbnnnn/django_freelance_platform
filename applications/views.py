from contextlib import closing

from django.shortcuts import render

from db.database import connect
from db.repository import _record


def index(request):
    with closing(connect()) as conn:
        rows = conn.execute("""
            SELECT a.*, o.name AS order_name, u.name AS executor_name,
                   u.second_name AS executor_second_name
            FROM applications AS a
            LEFT JOIN orders AS o ON o.id = a.order_id
            LEFT JOIN users AS u ON u.id = a.executor_id
            ORDER BY a.id;
        """).fetchall()
    return render(request, "applications/application_list.html", {
        "applications": [_record("applications", row) for row in rows],
    })


def detail(request, application_id):
    with closing(connect()) as conn:
        row = conn.execute("""
            SELECT a.*, o.name AS order_name, u.name AS executor_name,
                   u.second_name AS executor_second_name
            FROM applications AS a
            LEFT JOIN orders AS o ON o.id = a.order_id
            LEFT JOIN users AS u ON u.id = a.executor_id
            WHERE a.id = ?;
        """, (application_id,)).fetchone()
    if row is None:
        return render(request, "record_not_found.html", {
            "title": "Отклик не найден", "back_route": "applications:index",
        }, status=404)
    application = _record("applications", row)
    return render(request, "applications/application_detail.html", {"application": application})
