from django.shortcuts import render

from homepage.views import detail_page, detail_rows, not_found, object_link
from services.reviews import list_reviews


def index(request):
    return render(request, "reviews/review_list.html", {"reviews": list_reviews()})


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
