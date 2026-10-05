from django.http import HttpResponse


def index(request):
    return HttpResponse("Участники")


def detail(request, user_id):
    return HttpResponse(f"Участник №{user_id}")
