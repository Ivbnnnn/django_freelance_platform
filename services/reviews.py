from .utils import append_data, read_data


def create_review(order_id, author_id, rating, text):
    rating = int(rating)
    if not 1 <= rating <= 5:
        raise ValueError("Оценка 1-5")
    return append_data(
        "reviews.json",
        {"order_id": order_id, "author_id": author_id, "rating": rating, "text": text},
    )


def list_reviews():
    return read_data("reviews.json")
