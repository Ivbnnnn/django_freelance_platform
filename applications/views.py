from django.urls import reverse
from django.utils.html import format_html_join

from homepage.views import detail_page, detail_rows, list_page, not_found, object_link
from services.applications import list_applications


def index(request):
    items = format_html_join(
        "",
        '<a class="list-group-item list-group-item-action" href="{}">'
        '<strong>Отклик №{}</strong> · Заказ №{} · Исполнитель №{}</a>',
        (
            (reverse("applications:detail", kwargs={"application_id": item.id}), item.id, item.order_id, item.executor_id)
            for item in list_applications()
        ),
    )
    return list_page("Отклики", "Ответы исполнителей на опубликованные заказы.", items)


def detail(request, application_id):
    application = next((item for item in list_applications() if item.id == application_id), None)
    if application is None:
        return not_found("Отклик не найден", "applications:index")

    order_name = application.order.name if application.order else ""
    executor_name = (
        f"{application.executor.name} {application.executor.second_name}"
        if application.executor else ""
    )
    rows = detail_rows(
        ("ID", application.id),
        ("Заказ", object_link(application.order, application.order_id, "orders:detail", "order_id", order_name)),
        ("Исполнитель", object_link(
            application.executor, application.executor_id, "profiles:detail", "user_id", executor_name,
        )),
        ("Комментарий", application.comment or "Без комментария"),
    )
    return detail_page(f"Отклик №{application.id}", rows, "applications:index")
