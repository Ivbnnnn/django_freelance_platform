# Размещение заказа

order_name = input("Введите название заказа:")
order_price = input("Введите бюджет заказа:") #формата min-max, 1000-2000

def place_order(order_name: str, order_price: str):
    print(f"Ваш заказ {order_name} успешно размещен.")
    print(f"Ориентировочный бюджет равен: {order_price} рублей.")

place_order(order_name, order_price)