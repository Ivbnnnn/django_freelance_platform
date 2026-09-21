import pytest

from models import Serializable
from services.utils import append_data, read_data, write_data


def test_read_data_returns_empty_list_for_unknown_file():
    assert read_data("missing.json") == []


def test_write_data_serializes_and_read_data_restores_records(executor):
    saved = write_data("users.json", [executor])

    assert saved == [executor.to_dict()]
    assert read_data("users.json") == [executor.to_dict()]


def test_append_data_assigns_next_identifier():
    first = append_data("records.json", {"value": 1})
    second = append_data("records.json", {"value": 2})

    assert first["id"] == 1
    assert second["id"] == 2


def test_serializable_base_class_requires_conversion_method():
    with pytest.raises(NotImplementedError):
        Serializable().to_dict()
