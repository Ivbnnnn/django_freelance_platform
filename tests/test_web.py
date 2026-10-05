"""Проверки перехода от JSON-сервисов ПР3 к HTTP-страницам ПР5."""

import os

import django
import pytest
from django.test import Client
from django.urls import reverse

from services.applications import create_application
from services.orders import create_order
from services.reviews import create_review
from services.transactions import create_transaction
from services.users import create_user


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freelance_project.settings")
django.setup()


@pytest.fixture
def web_records(order, executor, customer):
    application = create_application(str(order.id), str(executor.id), "Готов выполнить")
    transaction = create_transaction(str(order.id), "5000")
    review = create_review(str(order.id), str(customer.id), 5, "Отлично")
    return order, application, transaction, review, customer, executor


def test_home_page_has_navigation_and_styles():
    response = Client().get("/")
    html = response.content.decode("utf-8")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/html")
    assert '<html lang="ru">' in html
    assert 'name="viewport"' in html
    assert "bootstrap@5.3.3" in html
    assert "/static/homepage/site.css" in html
    for section in ("orders", "applications", "transactions", "reviews", "profiles"):
        assert f'href="{reverse(f"{section}:index")}"' in html


def test_lists_use_existing_json_services(web_records):
    order, application, transaction, review, customer, executor = web_records
    pages = {
        "orders": (order.name, f"/orders/{order.id}/"),
        "applications": (f"Отклик №{application.id}", f"/applications/{application.id}/"),
        "transactions": (f"Платёж №{transaction.id}", f"/transactions/{transaction.id}/"),
        "reviews": (f"Отзыв №{review.id}", f"/reviews/{review.id}/"),
        "profiles": (executor.name, f"/profiles/{executor.id}/"),
    }
    client = Client()

    for section, (expected_text, detail_url) in pages.items():
        response = client.get(reverse(f"{section}:index"))
        html = response.content.decode("utf-8")
        assert response.status_code == 200
        assert expected_text in html
        assert f'href="{detail_url}"' in html


def test_detail_pages_show_related_objects(web_records):
    order, application, transaction, review, customer, executor = web_records
    client = Client()
    cases = (
        (f"/orders/{order.id}/", customer.name, f"/profiles/{customer.id}/"),
        (f"/applications/{application.id}/", order.name, f"/profiles/{executor.id}/"),
        (f"/transactions/{transaction.id}/", order.name, f"/orders/{order.id}/"),
        (f"/reviews/{review.id}/", review.text, f"/profiles/{customer.id}/"),
        (f"/profiles/{executor.id}/", executor.email, "/profiles/"),
    )

    for path, expected_text, related_url in cases:
        response = client.get(path)
        html = response.content.decode("utf-8")
        assert response.status_code == 200
        assert expected_text in html
        assert f'href="{related_url}"' in html


@pytest.mark.parametrize(
    "section",
    ("orders", "applications", "transactions", "reviews", "profiles"),
)
def test_unknown_detail_returns_404(section):
    response = Client().get(f"/{section}/999/")
    assert response.status_code == 404
    assert "Запись с таким ID не найдена" in response.content.decode("utf-8")


def test_empty_lists_are_readable():
    response = Client().get("/orders/")
    assert response.status_code == 200
    assert "Записей пока нет" in response.content.decode("utf-8")


def test_html_escapes_json_values_and_never_shows_password():
    user = create_user("<b>Имя</b>", "Тест", "Заказчик", "private-secret", "test@example.com")
    order = create_order("<script>alert(1)</script>", "100", str(user.id))
    client = Client()

    orders_html = client.get(f"/orders/{order.id}/").content.decode("utf-8")
    profile_html = client.get(f"/profiles/{user.id}/").content.decode("utf-8")
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in orders_html
    assert "<script>alert(1)</script>" not in orders_html
    assert "&lt;b&gt;Имя&lt;/b&gt;" in profile_html
    assert "private-secret" not in profile_html
