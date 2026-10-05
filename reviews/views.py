from django.urls import reverse
from django.utils.html import format_html_join

from homepage.views import detail_page, detail_rows, list_page, not_found, object_link
from services.reviews import list_reviews


def index(request):
    items = format_html_join(
        "",
        '<a class="list-group-item list-group-item-action" href="{}">'
        '<strong>Отзыв №{}</strong> · Заказ №{} · Оценка: {}/5</a>',
        (
            (reverse("reviews:detail", kwargs={"review_id": item.id}), item.id, item.order_id, item.rating)
            for item in list_reviews()
        ),
    )
    return list_page("Отзывы", "Оценки и впечатления участников о заказах.", items)


def detail(request, review_id):
    review = next((item for item in list_reviews() if item.id == review_id), None)
    if review is None:
        return not_found("Отзыв не найден", "reviews:index")

    order_name = review.order.name if review.order else ""
    author_name = f"{review.author.name} {review.author.second_name}" if review.author else ""
    rows = detail_rows(
        ("ID", review.id),
        ("Заказ", object_link(review.order, review.order_id, "orders:detail", "order_id", order_name)),
        ("Автор", object_link(review.author, review.author_id, "profiles:detail", "user_id", author_name)),
        ("Оценка", f"{review.rating}/5"),
        ("Текст", review.text or "Без текста"),
    )
    return detail_page(f"Отзыв №{review.id}", rows, "reviews:index")
