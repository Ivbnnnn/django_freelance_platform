from django.shortcuts import get_object_or_404, render

from .models import User


def index(request):
    records = User.objects.all()
    return render(request, 'profiles/profile_list.html', {'users': records})


def detail(request, user_id):
    record = get_object_or_404(User.objects.all(), pk=user_id)
    return render(request, 'profiles/profile_detail.html', {'user': record})
