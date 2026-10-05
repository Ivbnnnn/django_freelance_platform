from django.http import HttpResponse


def index(request):
    return HttpResponse("Отклики")


def detail(request, application_id):
    return HttpResponse(f"Отклик №{application_id}")
