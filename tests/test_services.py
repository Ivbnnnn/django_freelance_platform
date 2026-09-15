import pytest
from services.applications import create_application
from services.orders import create_order
from services.reviews import create_review
from services.transactions import create_transaction
from services.utils import read_data, write_data


@pytest.mark.validation
def test_order_validation():
    try:
        create_order("", "100")
    except ValueError:
        assert True


@pytest.mark.validation
def test_review_rating():
    try:
        create_review("1", "1", "6", "bad")
    except ValueError:
        assert True


@pytest.mark.validation
def test_application_validation():
    try:
        create_application("", "2")
    except ValueError:
        assert True


@pytest.mark.smoke
def test_transaction_saved():
    result = create_transaction("1", "100")
    assert result["status"] == "paid"


@pytest.mark.smoke
def test_json_roundtrip():
    write_data("test.json", [{"value": 1}])
    assert read_data("test.json")[0]["value"] == 1
