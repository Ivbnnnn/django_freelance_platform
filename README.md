# Сервис поиска исполнителей

Консольное приложение для публикации заказов, откликов, оплаты и отзывов.
В ПР3 функциональная модель из словарей преобразована в объектную.

## Объектная модель

| Класс | Данные | Основные методы |
| --- | --- | --- |
| `User` | id, имя, фамилия, email, роль | `check_password()`, `to_dict()` |
| `Customer`, `Executor` | специализированные пользователи | наследуют `User` |
| `Order` | id, название, бюджет, заказчик, статус | `assign_executor()`, `mark_paid()` |
| `Application` | id, заказ, исполнитель, комментарий | `accept()` |
| `Transaction` | id, заказ, сумма, статус | `pay()` |
| `Review` | id, заказ, автор, оценка, текст | `to_dict()` |

`Order`, `Application`, `Transaction` и `Review` хранят ссылки на связанные
объекты, если они присутствуют в хранилище. Например, `Application.accept()`
передаёт исполнителя заказу и переводит его в статус `in_progress`; оплата
переводит заказ в `paid`. Все классы реализуют `__str__` и `to_dict()`.

Пароль пользователя инкапсулирован в атрибуте `_password`; для проверки
предназначен метод `check_password()`. Подклассы `Customer` и `Executor`
демонстрируют наследование, а общее использование `User` — полиморфизм.

## Хранение данных

JSON-файлы находятся в `data/`. Модули сервисов загружают JSON-записи как
объекты соответствующих классов через `from_dict()` и сохраняют объекты через
`to_dict()`. В `services/utils.py` остались функции работы с внешним хранилищем.

## Структура

```
models/               # пакет классов предметной области
  __init__.py         # публичные импорты моделей
  user.py             # User, Customer, Executor
  order.py            # Order
  application.py      # Application
  transaction.py      # Transaction
  review.py           # Review
services/
  users.py           # коллекция пользователей
  orders.py          # коллекция заказов
  applications.py    # коллекция откликов
  transactions.py    # коллекция платежей
  reviews.py         # коллекция отзывов
  utils.py           # чтение и запись JSON
data/                # данные приложения
tests/               # pytest-тесты
main.py              # консольный интерфейс
```

Тесты разделены по ответственности: `test_users.py`, `test_orders.py`,
`test_applications.py`, `test_transactions.py` и `test_reviews.py`. Отдельные
файлы `test_utils.py` и `test_main.py` проверяют JSON-хранилище и консольный
интерфейс; общие изолированные фикстуры находятся в `conftest.py`.

## Запуск

```powershell
python main.py
pytest -v
flake8 .
```
