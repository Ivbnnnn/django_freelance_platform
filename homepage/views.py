"""Общий HTML-каркас и главная страница веб-интерфейса ПР5."""

from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html, format_html_join


SECTIONS = (
    ("homepage:index", "Главная"),
    ("orders:index", "Заказы"),
    ("applications:index", "Отклики"),
    ("transactions:index", "Платежи"),
    ("reviews:index", "Отзывы"),
    ("profiles:index", "Участники"),
)


def page(title, content):
    """Собрать общий HTML-документ без введения шаблонов до следующей работы."""
    navigation = format_html_join(
        "",
        '<a class="nav-link" href="{}">{}</a>',
        ((reverse(name), label) for name, label in SECTIONS),
    )
    stylesheet = staticfiles_storage.url("homepage/site.css")
    return format_html(
        """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Freelance</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="{stylesheet}">
</head>
<body>
  <nav class="navbar navbar-expand-lg bg-white border-bottom" aria-label="Основная навигация">
    <div class="container flex-wrap gap-2">
      <a class="navbar-brand fw-bold" href="{home}">Freelance</a>
      <div class="nav flex-wrap">{navigation}</div>
    </div>
  </nav>
  <main class="container py-4 py-md-5">{content}</main>
</body>
</html>""",
        title=title,
        stylesheet=stylesheet,
        home=reverse("homepage:index"),
        navigation=navigation,
        content=content,
    )


def html_response(title, content, status=200):
    return HttpResponse(page(title, content), status=status)


def list_page(title, description, items):
    body = format_html(
        '<header class="mb-4"><h1>{}</h1><p class="lead text-muted">{}</p></header>'
        '<div class="list-group">{}</div>',
        title,
        description,
        items or format_html('<p class="text-muted">{}</p>', "Записей пока нет."),
    )
    return html_response(title, body)


def detail_row(label, value):
    return format_html('<dt class="col-sm-3">{}</dt><dd class="col-sm-9">{}</dd>', label, value)


def detail_rows(*pairs):
    return format_html_join("", "{}", ((detail_row(label, value),) for label, value in pairs))


def detail_page(title, rows, back_route):
    body = format_html(
        '<a class="link-secondary" href="{}">← К списку</a>'
        '<h1 class="mt-3 mb-4">{}</h1>'
        '<div class="card shadow-sm"><div class="card-body"><dl class="row mb-0">{}</dl></div></div>',
        reverse(back_route),
        title,
        rows,
    )
    return html_response(title, body)


def not_found(title, back_route):
    body = format_html(
        '<h1 class="text-danger">{}</h1><p>Запись с таким ID не найдена.</p>'
        '<a class="btn btn-outline-secondary" href="{}">К списку</a>',
        title,
        reverse(back_route),
    )
    return html_response(title, body, status=404)


def object_link(obj, object_id, route, key, label):
    """Показывать ссылку лишь для существующего связанного объекта."""
    if obj is not None:
        return format_html('<a href="{}">{}</a>', reverse(route, kwargs={key: obj.id}), label)
    if object_id:
        return format_html('№{} (запись отсутствует)', object_id)
    return "Не указан"


def status_badge(status):
    styles = {
        "new": ("Новый", "text-bg-primary"),
        "in_progress": ("В работе", "text-bg-warning"),
        "paid": ("Оплачен", "text-bg-success"),
    }
    label, style = styles.get(status, (status, "text-bg-secondary"))
    return format_html('<span class="badge {}">{}</span>', style, label)


def index(request):
    links = format_html_join(
        "",
        '<a class="btn btn-outline-primary" href="{}">{}</a>',
        ((reverse(name), label) for name, label in SECTIONS[1:]),
    )
    body = format_html(
        '<section class="hero rounded-4 p-4 p-md-5">'
        '<h1 class="display-5 fw-bold mb-4">Сервис поиска исполнителей</h1>'
        '<div class="d-flex flex-wrap gap-2">{}</div></section>',
        links,
    )
    return html_response("Главная", body)
