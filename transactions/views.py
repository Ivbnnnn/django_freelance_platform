from django.http import HttpResponse


def index(request):
    return HttpResponse("Платежи")


def detail(request, transaction_id):
    return HttpResponse(f"Платёж №{transaction_id}")
