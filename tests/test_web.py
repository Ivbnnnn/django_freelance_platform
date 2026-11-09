"""SQLite import and Django page integration."""

import json
import os

import django
import pytest
from django.test import Client
from django.core.management import call_command

from db import database, import_json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freelance_project.settings")
django.setup()


@pytest.fixture
def web_database(tmp_path, monkeypatch, db):
    source = tmp_path / "source"
    source.mkdir()
    samples = {
        "users": [
            {"id": 1, "name": "Анна", "second_name": "Петрова", "role": "Заказчик",
             "password": "private-secret", "email": "a@example.com"},
            {"id": 2, "name": "Иван", "second_name": "Иванов", "role": "Исполнитель",
             "password": "secret", "email": "i@example.com"}],
        "orders": [
            {"id": 1, "name": "<b>Логотип</b>", "budget": "5000", "customer_id": "1",
             "status": "new"},
            {"id": 2, "name": "Сайт", "budget": "9000", "customer_id": "1",
             "status": "paid"}],
        "applications": [
            {"id": 1, "order_id": "1", "executor_id": "2", "comment": ""},
            {"id": 2, "order_id": "999", "executor_id": "2", "comment": "Готов"}],
        "transactions": [
            {"id": 1, "order_id": "2", "amount": "9000", "status": "paid"}],
        "reviews": [
            {"id": 1, "order_id": "2", "author_id": "1", "rating": 5,
             "text": "Отлично"}],
    }
    for name, rows in samples.items():
        (source / f"{name}.json").write_text(
            json.dumps(rows, ensure_ascii=False), encoding="utf-8",
        )
    monkeypatch.setattr(import_json, "DATA", source)
    path = tmp_path / "freelance.sqlite"
    import_json.import_data(path)
    monkeypatch.setattr(database, "DATABASE", path)
    call_command("import_legacy", source=path)
    return path


def test_pages_show_orm_data(web_database):
    client = Client()
    pages = [
        ("/", "Поиск заказов"), ("/orders/", "Логотип"),
        ("/applications/", "Отклик №1"),
        ("/transactions/", "Платёж №1"), ("/reviews/", "Отзыв №1"),
        ("/profiles/", "Анна"), ("/orders/1/", "Петрова"),
        ("/applications/1/", "Иванов"), ("/transactions/1/", "Сайт"),
        ("/reviews/1/", "Отлично"), ("/profiles/1/", "a@example.com"),
    ]
    for url, expected in pages:
        response = client.get(url)
        assert response.status_code == 200
        assert expected in response.content.decode()


def test_missing_links_and_404(web_database):
    client = Client()
    html = client.get("/applications/2/").content.decode()
    assert "№999 (запись отсутствует)" in html
    assert 'href="/orders/999/"' not in html
    for path in ("/orders/999/", "/applications/999/", "/profiles/999/",
                 "/transactions/999/", "/reviews/999/", "/unknown"):
        assert client.get(path).status_code == 404
    assert "Страница не найдена" in client.get("/unknown").content.decode()


def test_search_and_statistics(web_database):
    client = Client()
    search = client.get("/orders/search/", {"q": "Логотип"}).content.decode()
    assert "Логотип" in search and "Сайт" not in search
    assert "Найдено: 0" in client.get("/orders/search/", {"q": "%"}).content.decode()
    stats = client.get("/orders/statistics/").content.decode()
    assert "Всего заказов: 2" in stats
    assert "Откликов: 2" in stats
    assert "9000" in stats


def test_html_escaping_and_foreign_keys(web_database):
    client = Client()
    html = client.get("/orders/1/").content.decode()
    assert "&lt;b&gt;Логотип&lt;/b&gt;" in html
    assert "<b>Логотип</b>" not in html
    assert "private-secret" not in client.get("/profiles/1/").content.decode()
    assert "Без комментария" in client.get("/applications/1/").content.decode()
    with database.connect() as connection:
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
