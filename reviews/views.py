from django.shortcuts import render

from services.reviews import list_reviews


def index(request):
    return render(request, "reviews/review_list.html", {"reviews": list_reviews()})


def detail(request, review_id):
    review = next((item for item in list_reviews() if item.id == review_id), None)
    if review is None:
        return render(request, "record_not_found.html", {
            "title": "Отзыв не найден", "back_route": "reviews:index",
        }, status=404)
    return render(request, "reviews/review_detail.html", {"review": review})
