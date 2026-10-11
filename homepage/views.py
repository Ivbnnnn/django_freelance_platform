"""Главная страница сервиса поиска исполнителей."""

from django.shortcuts import render


def index(request):
    return render(request, "homepage/index.html")
