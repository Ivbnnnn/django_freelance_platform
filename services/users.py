from .utils import append_data, read_data

def create_user(name, second_name, role, password, email):
    if not all((name, second_name, role, password, email)):
        raise ValueError("Все поля обязательны")
    if role not in ("Исполнитель", "Заказчик"):
        raise ValueError("Некорректная роль")
    return append_data("users.json", {"name": name, "second_name": second_name, "role": role, "password": password, "email": email})

def list_users():
    return read_data("users.json")
