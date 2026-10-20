from contextlib import closing

from django.shortcuts import render

from db.database import connect
from db.repository import _record


def index(request):
    with closing(connect()) as conn:
        rows = conn.execute("""
            SELECT r.*, o.name AS order_name, u.name AS author_name
            FROM reviews AS r
            LEFT JOIN orders AS o ON o.id = r.order_id
            LEFT JOIN users AS u ON u.id = r.author_id
            ORDER BY r.id;
        """).fetchall()
    return render(request, "reviews/review_list.html", {
        "reviews": [_record("reviews", row) for row in rows],
    })


def detail(request, review_id):
    with closing(connect()) as conn:
        row = conn.execute("""
            SELECT r.*, o.name AS order_name, u.name AS author_name
            FROM reviews AS r
            LEFT JOIN orders AS o ON o.id = r.order_id
            LEFT JOIN users AS u ON u.id = r.author_id
            WHERE r.id = ?;
        """, (review_id,)).fetchone()
    if row is None:
        return render(request, "record_not_found.html", {
            "title": "Отзыв не найден", "back_route": "reviews:index",
        }, status=404)
    review = _record("reviews", row)
    return render(request, "reviews/review_detail.html", {"review": review})
