import pytest

from services import utils
from services.orders import create_order
from services.users import create_user


@pytest.fixture(autouse=True)
def temporary_data_dir(tmp_path, monkeypatch):
    """Использует изолированные JSON-файлы, не меняя данные приложения."""
    monkeypatch.setattr(utils, "DATA_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def executor():
    return create_user("Иван", "Иванов", "Исполнитель", "secret", "i@mail.ru")


@pytest.fixture
def customer():
    return create_user("Анна", "Петрова", "Заказчик", "secret", "a@mail.ru")


@pytest.fixture
def order(customer):
    return create_order("Логотип", "5000", str(customer.id))
