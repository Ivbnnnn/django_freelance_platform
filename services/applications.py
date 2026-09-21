from models import Application
from .orders import list_orders
from .users import list_users
from .utils import read_data, write_data


def list_applications() -> list[Application]:
    orders = {str(order.id): order for order in list_orders()}
    users = {str(user.id): user for user in list_users()}
    return [
        Application.from_dict(record, orders, users)
        for record in read_data("applications.json")
    ]


def create_application(
    order_id: str, executor_id: str, comment: str = ""
) -> Application:
    applications = list_applications()
    orders = {str(order.id): order for order in list_orders()}
    users = {str(user.id): user for user in list_users()}
    application = Application(
        application_id=max((item.id for item in applications), default=0) + 1,
        order=orders.get(str(order_id)),
        executor=users.get(str(executor_id)),
        comment=comment,
        order_id=str(order_id),
        executor_id=str(executor_id),
    )
    applications.append(application)
    write_data("applications.json", applications)
    return application
