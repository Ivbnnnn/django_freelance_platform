from contextlib import closing

from django.shortcuts import render

from db.database import connect
from db.repository import _record


def index(request):
    with closing(connect()) as conn:
        rows = conn.execute("""
            SELECT id, name, second_name, role, email
            FROM users ORDER BY id;
        """).fetchall()
    return render(request, "profiles/profile_list.html", {
        "users": [_record("users", row) for row in rows],
    })


def detail(request, user_id):
    with closing(connect()) as conn:
        row = conn.execute("""
            SELECT id, name, second_name, role, email
            FROM users WHERE id = ?;
        """, (user_id,)).fetchone()
    if row is None:
        return render(request, "record_not_found.html", {
            "title": "Участник не найден", "back_route": "profiles:index",
        }, status=404)
    user = _record("users", row)
    return render(request, "profiles/profile_detail.html", {"user": user})
