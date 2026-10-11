from django.shortcuts import render

from homepage.views import detail_page, detail_rows, not_found
from services.users import list_users


def index(request):
    return render(request, "profiles/profile_list.html", {"users": list_users()})


def detail(request, user_id):
    user = next((item for item in list_users() if item.id == user_id), None)
    if user is None:
        return not_found("Участник не найден", "profiles:index")

    rows = detail_rows(
        ("ID", user.id),
        ("Имя", user.name),
        ("Фамилия", user.second_name),
        ("Роль", user.role),
        ("Email", user.email),
    )
    return detail_page(f"Участник №{user.id}", rows, "profiles:index")
