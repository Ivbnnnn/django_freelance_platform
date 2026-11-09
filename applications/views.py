from django.shortcuts import get_object_or_404, render

from .models import Application


def index(request):
    records = Application.objects.all().select_related('order', 'executor')
    return render(request, 'applications/application_list.html', {'applications': records})


def detail(request, application_id):
    record = get_object_or_404(Application.objects.select_related('order', 'executor'), pk=application_id)
    return render(request, 'applications/application_detail.html', {'application': record})
