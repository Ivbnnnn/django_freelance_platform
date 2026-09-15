from services.applications import create_application, list_applications
from services.orders import create_order, list_orders
from services.reviews import create_review, list_reviews
from services.transactions import create_transaction, list_transactions
from services.users import create_user, list_users


def show_items(items):
    if items:
        print(*items, sep="\n")
    else:
        print("Заказов пока нет.")


def main():
    while True:
        print(
            "1 user 2 order 3 orders 4 application 5 payment 6 review 7 users 8 applications 9 payments 10 reviews 0 exit"
        )
        choice = input("Action: ").strip()
        try:
            if choice == "0":
                break
            if choice == "1":
                print(
                    create_user(
                        input("Name: "),
                        input("Surname: "),
                        input("Role: "),
                        input("Password: "),
                        input("Email: "),
                    )
                )
            elif choice == "2":
                print(
                    create_order(
                        input("Name: "), input("Budget: "), input("Customer id: ")
                    )
                )
            elif choice == "3":
                show_items(list_orders())
            elif choice == "4":
                print(
                    create_application(
                        input("Order id: "), input("Executor id: "), input("Comment: ")
                    )
                )
            elif choice == "5":
                print(create_transaction(input("Order id: "), input("Amount: ")))
            elif choice == "6":
                print(
                    create_review(
                        input("Order id: "),
                        input("Author id: "),
                        input("Rating: "),
                        input("Text: "),
                    )
                )
            elif choice == "7":
                print(*list_users(), sep="\n")
            elif choice == "8":
                print(*list_applications(), sep="\n")
            elif choice == "9":
                print(*list_transactions(), sep="\n")
            elif choice == "10":
                print(*list_reviews(), sep="\n")
            else:
                print("Unknown command")
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
