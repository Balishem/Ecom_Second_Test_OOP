

from models.customer import Customer, CustomerType
from models.order_item import OrderItem
from models.order import Order, VIPOrder, PaymentType


def main():
    regular_customer = Customer(
        1, "Alex", "Smith",
        "alex@example.com", "Tel Aviv"
    )

    vip_customer = Customer(
        2, "Oleg", "Byashimov",
        "oleg@example.com", "Lod",
        CustomerType.VIP, 15
    )

    laptop = OrderItem(1, "Laptop", 3500)
    mouse = OrderItem(2, "Mouse", 150)
    keyboard = OrderItem(3, "Keyboard", 300)

    regular_order = Order(
        101,
        "Regular Purchase",
        "Tel Aviv",
        [laptop, mouse],
        regular_customer,
        PaymentType.CASH,
    )

    vip_order = VIPOrder(
        102,
        "VIP Purchase",
        "Lod",
        [laptop, keyboard],
        vip_customer,
        PaymentType.CREDIT_CARD,
    )

    print(regular_order)
    print(vip_order)

    print("Regular total:", regular_order.total_price)
    print("VIP total:", vip_order.total_price)

    print("Regular favorites:", regular_customer.favorite_items)
    print("VIP favorites:", vip_customer.favorite_items)


if __name__ == "__main__":
    main()
