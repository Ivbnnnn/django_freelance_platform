from django.shortcuts import render

from services.applications import list_applications


def index(request):
    return render(request, "applications/application_list.html", {"applications": list_applications()})


def detail(request, application_id):
    application = next((item for item in list_applications() if item.id == application_id), None)
    if application is None:
        return render(request, "record_not_found.html", {
            "title": "Отклик не найден", "back_route": "applications:index",
        }, status=404)
    return render(request, "applications/application_detail.html", {"application": application})
