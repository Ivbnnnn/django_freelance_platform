import pytest

from services.applications import create_application, list_applications
from models import Application, Order


def test_create_application_links_order_and_executor(order, executor):
    application = create_application(str(order.id), str(executor.id), "Готов выполнить")

    assert isinstance(application, Application)
    assert application.order.id == order.id
    assert application.executor.id == executor.id


def test_list_applications_loads_objects(order, executor):
    create_application(str(order.id), str(executor.id))

    assert isinstance(list_applications()[0], Application)


def test_application_accepts_and_serializes(order, executor):
    application = Application(1, order, executor, "Комментарий")
    application.accept()
    restored = Application.from_dict(
        application.to_dict(), {str(order.id): order}, {str(executor.id): executor}
    )

    assert order.status == Order.STATUS_IN_PROGRESS
    assert restored.order_id == str(order.id)
    assert restored.executor_id == str(executor.id)
    assert "Отклик" in str(restored)


def test_application_rejects_missing_or_invalid_executor(order, customer):
    with pytest.raises(ValueError):
        create_application("", "1")
    with pytest.raises(ValueError):
        Application(1, order, customer)
    with pytest.raises(ValueError):
        Application(1, None, None, order_id="1", executor_id="1").accept()
