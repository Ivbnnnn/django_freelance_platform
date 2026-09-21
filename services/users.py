from models import User
from .utils import read_data, write_data


def list_users() -> list[User]:
    """Загружает записи JSON как объекты пользователей."""
    return [User.from_dict(record) for record in read_data("users.json")]


def create_user(
    name: str, second_name: str, role: str, password: str, email: str
) -> User:
    users = list_users()
    user = User.create(
        id=max((item.id for item in users), default=0) + 1,
        name=name,
        second_name=second_name,
        role=role,
        password=password,
        email=email,
    )
    users.append(user)
    write_data("users.json", users)
    return user
