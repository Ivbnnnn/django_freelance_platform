from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("statistics/", views.stats, name="statistics"),
    path("<int:order_id>/", views.detail, name="detail"),
]
