from django.shortcuts import get_object_or_404, render

from .models import Review


def index(request):
    records = Review.objects.all().select_related('order', 'author')
    return render(request, 'reviews/review_list.html', {'reviews': records})


def detail(request, review_id):
    record = get_object_or_404(Review.objects.select_related('order', 'author'), pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': record})
