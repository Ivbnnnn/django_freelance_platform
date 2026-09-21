import pytest

from models import Customer, Executor, User
from services.users import create_user, list_users


def test_create_user_returns_role_specific_object():
    user = create_user("Иван", "Иванов", User.EXECUTOR, "secret", "i@mail.ru")

    assert isinstance(user, Executor)
    assert user.id == 1


def test_list_users_loads_objects_from_json(executor, customer):
    users = list_users()

    assert [user.id for user in users] == [executor.id, customer.id]
    assert isinstance(users[0], Executor)
    assert isinstance(users[1], Customer)


def test_user_factory_and_serialization():
    data = {
        "id": 4,
        "name": "Анна",
        "second_name": "Петрова",
        "role": User.CUSTOMER,
        "password": "secret",
        "email": "a@mail.ru",
    }

    user = User.create(**data)
    restored = User.from_dict(data)

    assert isinstance(user, Customer)
    assert isinstance(restored, Customer)
    assert user.to_dict() == data
    assert user["email"] == "a@mail.ru"
    assert user.check_password("secret")
    assert not user.check_password("wrong")
    assert "Анна Петрова" in str(user)


@pytest.mark.parametrize("role", ("", "Администратор"))
def test_user_rejects_invalid_data(role):
    with pytest.raises(ValueError):
        User(1, "Иван", "Иванов", role, "secret", "i@mail.ru")
