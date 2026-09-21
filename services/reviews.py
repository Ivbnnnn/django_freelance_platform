from models import Review
from .orders import list_orders
from .users import list_users
from .utils import read_data, write_data


def list_reviews() -> list[Review]:
    orders = {str(order.id): order for order in list_orders()}
    users = {str(user.id): user for user in list_users()}
    return [Review.from_dict(record, orders, users) for record in read_data("reviews.json")]


def create_review(order_id: str, author_id: str, rating: int | str, text: str) -> Review:
    reviews = list_reviews()
    orders = {str(order.id): order for order in list_orders()}
    users = {str(user.id): user for user in list_users()}
    review = Review(
        review_id=max((item.id for item in reviews), default=0) + 1,
        order=orders.get(str(order_id)),
        author=users.get(str(author_id)),
        rating=int(rating),
        text=text,
        order_id=str(order_id),
        author_id=str(author_id),
    )
    reviews.append(review)
    write_data("reviews.json", reviews)
    return review
