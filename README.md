# Сервис поиска исполнителей

Учебный проект для публикации заказов, откликов исполнителей, платежей и отзывов. В ПР3 были созданы объектная модель, JSON-хранилище, консольное меню и тесты. ПР5 добавляет к тому же репозиторию веб-интерфейс на **Django 5.2**, сохраняя консольную версию и данные.

## Что можно посмотреть в браузере

| Страница | URL | View-функция |
| --- | --- | --- |
| Главная и навигация | `/` | `homepage.views.index` |
| Список заказов | `/orders/` | `orders.views.index` |
| Карточка заказа | `/orders/<int:order_id>/` | `orders.views.detail` |
| Список откликов | `/applications/` | `applications.views.index` |
| Карточка отклика | `/applications/<int:application_id>/` | `applications.views.detail` |
| Список платежей | `/transactions/` | `transactions.views.index` |
| Карточка платежа | `/transactions/<int:transaction_id>/` | `transactions.views.detail` |
| Список отзывов | `/reviews/` | `reviews.views.index` |
| Карточка отзыва | `/reviews/<int:review_id>/` | `reviews.views.detail` |
| Список участников | `/profiles/` | `profiles.views.index` |
| Карточка участника | `/profiles/<int:user_id>/` | `profiles.views.detail` |

Маршруты с числовым ID открывают запись из JSON-хранилища; если записи нет, возвращается HTML-страница с кодом **404**. Ссылки связывают заказ с заказчиком, отклик с заказом и исполнителем, платёж с заказом, отзыв с заказом и автором. Пароли на страницах не показываются.

## Структура

```text
manage.py                 точка входа Django
freelance_project/         настройки проекта и корневые URL
homepage/                  главная страница, общий HTML-каркас, CSS
orders/                    страницы заказов
applications/              страницы откликов
transactions/              страницы платежей
reviews/                   страницы отзывов
profiles/                  страницы участников
models/                    классы предметной области из ПР3
services/                  загрузка, связывание и сохранение объектов
data/                      JSON-файлы существующего проекта
main.py                    консольное приложение из ПР3
tests/                     тесты консольной и веб-части
```

В `freelance_project/urls.py` подключены маршруты приложений; конкретные адреса определены в их `urls.py`. View-функции читают объекты через существующие функции `services/`, находят запись по ID и возвращают `HttpResponse`. Общий HTML-документ собирает `homepage.views.page()`. Динамические значения экранируются при выводе. Страницы используют HTML, Bootstrap 5.3.3 через CDN и собственный файл `homepage/static/homepage/site.css`.

На этапе ПР5 объекты `User`, `Order`, `Application`, `Transaction` и `Review` остаются обычными классами Python из `models/`; данные хранятся в `data/*.json`. Веб-страницы только читают данные. Django ORM, шаблоны, веб-формы и аутентификация будут добавляться на следующих этапах.

## Запуск

Нужен Python 3.11 или новее. Из корня репозитория в PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Откройте <http://127.0.0.1:8000/>. Для показанных страниц миграции базы данных не нужны: источник данных — JSON-файлы. Консольный вариант по-прежнему запускается командой `python main.py`.

## Проверки

```powershell
python -m pytest -v
python -m flake8 .
```

`tests/test_web.py` проверяет маршруты, навигацию, данные из сервисов, связи объектов, ответы 404, экранирование HTML и отсутствие пароля в ответе. Остальные тесты проверяют код ПР3. Настройки локализации Django: русский язык и часовой пояс `Europe/Moscow`.
