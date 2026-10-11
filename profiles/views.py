from django.shortcuts import render

from services.users import list_users


def index(request):
    return render(request, "profiles/profile_list.html", {"users": list_users()})


def detail(request, user_id):
    user = next((item for item in list_users() if item.id == user_id), None)
    if user is None:
        return render(request, "record_not_found.html", {
            "title": "Участник не найден", "back_route": "profiles:index",
        }, status=404)
    return render(request, "profiles/profile_detail.html", {"user": user})
