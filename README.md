# Сервис поиска исполнителей

Учебный проект ПР3–ПР7: заказчики размещают заказы, исполнители оставляют отклики, а сервис показывает платежи и отзывы. ПР6 использует шаблоны Django; ПР7 добавляет прямую работу с SQLite через `sqlite3`, без Django ORM. Консольное приложение и исходные JSON-файлы сохранены.

## Запуск

Требуются Python 3.11+ и зависимости из `requirements.txt`.

```powershell
python -m pip install -r requirements.txt
python -m db.import_json
python manage.py check
python manage.py runserver
```

Откройте <http://127.0.0.1:8000/>. Импорт создаёт или обновляет `data/freelance.sqlite` из `data/*.json`. Его следует повторить после изменения JSON. Django-миграции для этих страниц не нужны. Консольная версия запускается командой `python main.py` и продолжает работать с JSON.

## Страницы

| Раздел | Адрес |
| --- | --- |
| Главная | `/` |
| Заказы и карточка | `/orders/`, `/orders/<id>/` |
| Поиск новых заказов по названию | `/orders/search/?q=...` |
| Статистика статусов, откликов и платежей | `/orders/statistics/` |
| Отклики и карточка | `/applications/`, `/applications/<id>/` |
| Платежи и карточка | `/transactions/`, `/transactions/<id>/` |
| Отзывы и карточка | `/reviews/`, `/reviews/<id>/` |
| Участники и карточка | `/profiles/`, `/profiles/<id>/` |

Все страницы читают данные из SQLite. Несуществующий ID даёт ответ 404. Отсутствующие связанные записи отображаются без ошибочной ссылки. Пароли пользователей в HTML не выводятся.

## Слой базы данных

`sql/schema.sql` создаёт пять таблиц. `db/database.py` открывает соединение с проверкой внешних ключей и возвращает именованные результаты `sqlite3.Row`. `db/import_json.py` переносит исходные записи пакетными вставками. Исторические ссылки на отсутствующие объекты сохраняются как текстовые `source_*_id`, а соответствующие внешние ключи остаются `NULL`; поэтому импорт не теряет отклики и отзывы с некорректными ссылками.

| Таблица | Поля (тип) | Ключи |
| --- | --- | --- |
| `users` | `id INTEGER`, `name TEXT`, `second_name TEXT`, `role TEXT`, `password TEXT`, `email TEXT` | `id` PK |
| `orders` | `id INTEGER`, `name TEXT`, `budget TEXT`, `customer_id INTEGER`, `source_customer_id TEXT`, `status TEXT` | `id` PK; `customer_id` → `users.id` |
| `applications` | `id INTEGER`, `order_id INTEGER`, `executor_id INTEGER`, `source_order_id TEXT`, `source_executor_id TEXT`, `comment TEXT` | `id` PK; `order_id` → `orders.id`; `executor_id` → `users.id` |
| `transactions` | `id INTEGER`, `order_id INTEGER`, `source_order_id TEXT`, `amount TEXT`, `status TEXT` | `id` PK; `order_id` → `orders.id` |
| `reviews` | `id INTEGER`, `order_id INTEGER`, `author_id INTEGER`, `source_order_id TEXT`, `source_author_id TEXT`, `rating INTEGER`, `text TEXT` | `id` PK; `order_id` → `orders.id`; `author_id` → `users.id` |

`sql/queries.sql` содержит 16 проверяемых запросов: списки, выборку по ID и поиск с `WHERE`, связи через `JOIN`, подсчёты через `COUNT`, группировки `GROUP BY`, сумму платежей. Как в примере ПР7, Django-представления содержат SQL непосредственно в `views.py` и выполняют его через `sqlite3` с параметрами `?`; файл `queries.sql` оставлен как перечень запросов для проверки. `db/repository.py` сохраняет преобразование строк результата для существующих шаблонов. Страницы поиска и статистики дают пользовательские сценарии для фильтрации и агрегации. Для поиска свободных помещений из примера методички здесь используется соответствующий предметной области поиск новых заказов; дата у заказов отсутствует.

Шаблоны используют `base.html`, `{% extends %}`, `{% block %}`, `{% include %}`, контекст, циклы, условия, фильтры, `{% url %}` и `{% static %}`. CSS, JavaScript и логотип находятся в `homepage/static/homepage/`.

## Проверка

```powershell
python manage.py check
python -m pytest -q
python -m flake8 . --extend-exclude=dvenv
```

`tests/test_web.py` проверяет SQL-страницы, поиск, статистику, внешние ключи, 404, экранирование HTML и отсутствие пароля. Остальные тесты проверяют объектную и консольную части проекта.
