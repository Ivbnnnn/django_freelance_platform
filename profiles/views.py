from django.urls import reverse
from django.utils.html import format_html_join

from homepage.views import detail_page, detail_rows, list_page, not_found
from services.users import list_users


def index(request):
    items = format_html_join(
        "",
        '<a class="list-group-item list-group-item-action" href="{}">'
        '<strong>{} {}</strong> · {}</a>',
        (
            (reverse("profiles:detail", kwargs={"user_id": user.id}), user.name, user.second_name, user.role)
            for user in list_users()
        ),
    )
    return list_page("Участники", "Заказчики и исполнители проекта.", items)


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
