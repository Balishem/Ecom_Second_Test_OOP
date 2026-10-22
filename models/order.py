
from datetime import datetime
from enum import Enum

from models.customer import Customer, CustomerType
from models.order_item import OrderItem


class PaymentType(Enum):
    CREDIT_CARD = "CREDIT CARD"
    CASH = "CASH"
    CHECK = "CHECK"
    OTHER = "OTHER"


class Order:
    _used_ids = set()

    def __init__(
        self,
        order_id: int,
        name: str,
        delivery_address: str,
        items: list[OrderItem],
        customer: Customer,
        payment_type: PaymentType,
        order_date: datetime | None = None,
    ):
        if not isinstance(order_id, int) or isinstance(order_id, bool):
            raise TypeError("Order ID must be an integer")

        if order_id in Order._used_ids:
            raise ValueError(f"Order ID {order_id} already exists")

        if not isinstance(customer, Customer):
            raise TypeError("Customer must be a Customer object")

        if not isinstance(payment_type, PaymentType):
            raise TypeError("Invalid payment type")

        if not all(isinstance(item, OrderItem) for item in items):
            raise TypeError("All items must be OrderItem objects")

        item_ids = [item.id for item in items]

        if len(item_ids) != len(set(item_ids)):
            raise ValueError("Item IDs must be unique within an order")

        self.__id = order_id
        self.__name = name
        self.__delivery_address = delivery_address
        self.__items = items.copy()
        self.__customer = customer
        self.__payment_type = payment_type
        self.__order_date = order_date or datetime.now()

        # Constructor calculates the total price.
        self.__total_price = self.calculate_total_price()

        # Register ID only after successful calculation.
        Order._used_ids.add(order_id)

        # Automatically update customer's favorite items.
        for item in self.__items:
            self.__customer.add_favorite_item(item)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def delivery_address(self):
        return self.__delivery_address

    @property
    def items(self):
        return self.__items.copy()

    @property
    def customer(self):
        return self.__customer

    @property
    def total_price(self):
        return self.__total_price

    @property
    def payment_type(self):
        return self.__payment_type

    @property
    def order_date(self):
        return self.__order_date

    def calculate_total_price(self):
        return sum(item.price for item in self.__items)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.__id}, "
            f"name={self.__name!r}, "
            f"total={self.__total_price:.2f})"
        )


class VIPOrder(Order):
    def __init__(
        self,
        order_id: int,
        name: str,
        delivery_address: str,
        items: list[OrderItem],
        customer: Customer,
        payment_type: PaymentType,
        order_date: datetime | None = None,
    ):
        if not isinstance(customer, Customer):
            raise TypeError("Customer must be a Customer object")

        if customer.customer_type != CustomerType.VIP:
            raise ValueError("Only VIP customers can create VIP orders")

        super().__init__(
            order_id,
            name,
            delivery_address,
            items,
            customer,
            payment_type,
            order_date,
        )

    def calculate_total_price(self):
        original_price = super().calculate_total_price()
        discount = self.customer.discount or 0

        return original_price * (1 - discount / 100)
