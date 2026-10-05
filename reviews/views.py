from django.http import HttpResponse


def index(request):
    return HttpResponse("Отзывы")


def detail(request, review_id):
    return HttpResponse(f"Отзыв №{review_id}")
