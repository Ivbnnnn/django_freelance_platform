import pytest

from models import Review
from services.reviews import create_review, list_reviews


def test_create_review_links_order_and_author(order, customer):
    review = create_review(str(order.id), str(customer.id), 5, "Отлично")

    assert isinstance(review, Review)
    assert review.order.id == order.id
    assert review.author.id == customer.id


def test_list_reviews_loads_objects(order, customer):
    create_review(str(order.id), str(customer.id), 5, "Отлично")

    assert isinstance(list_reviews()[0], Review)


def test_review_serialization_and_string_representation(order, customer):
    review = Review(1, order, customer, 4, "Хорошо")
    restored = Review.from_dict(
        review.to_dict(), {str(order.id): order}, {str(customer.id): customer}
    )

    assert restored.order_id == str(order.id)
    assert restored.author_id == str(customer.id)
    assert restored["rating"] == 4
    assert "Отзыв" in str(restored)


@pytest.mark.parametrize("rating", (0, 6))
def test_review_rejects_invalid_rating(order, customer, rating):
    with pytest.raises(ValueError):
        create_review(str(order.id), str(customer.id), rating, "Текст")
