
from enum import Enum
from models.gift import GiftInterface
from models.order_item import OrderItem
import math


class CustomerType(Enum):
    REGULAR = "REGULAR"
    VIP = "VIP"


class Customer:
    _used_ids = set()

    @classmethod
    def reset_ids(cls):
        """Forget all registered customer IDs (useful for tests)."""
        cls._used_ids.clear()

    def __init__(
        self,
        customer_id: int,
        first_name: str,
        last_name: str,
        email: str,
        delivery_address: str,
        customer_type: CustomerType = CustomerType.REGULAR,
        discount: float | None = None,
    ):
        """Create a customer.

        discount is a PERCENTAGE between 0 and 100 (15 means 15% off),
        or None for no discount. It is only applied to VIP orders.
        """
        if not isinstance(customer_id, int) or isinstance(customer_id, bool):
            raise TypeError("Customer ID must be an integer")

        if customer_id in Customer._used_ids:
            raise ValueError(f"Customer ID {customer_id} already exists")

        if not isinstance(customer_type, CustomerType):
            raise TypeError("Invalid customer type")

        if discount is not None:
            if isinstance(discount, bool) or not isinstance(discount, (int, float)):
                raise TypeError("Discount must be a number")

            if not math.isfinite(discount) or not 0 <= discount <= 100:
                raise ValueError("Discount must be between 0 and 100")

        self.__id = customer_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__delivery_address = delivery_address
        self.__customer_type = customer_type
        self.__discount = discount
        self.__favorite_items = []
        self.__gift = None

        Customer._used_ids.add(customer_id)

    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def email(self):
        return self.__email

    @property
    def delivery_address(self):
        return self.__delivery_address

    @property
    def customer_type(self):
        return self.__customer_type

    @property
    def discount(self):
        return self.__discount

    @property
    def favorite_items(self):
        return self.__favorite_items.copy()

    @property
    def gift(self):
        return self.__gift

    def add_favorite_item(self, item):
        if not isinstance(item, OrderItem):
            raise TypeError("Favorite item must be an OrderItem")

        if not any(
                favorite.name == item.name
                for favorite in self.__favorite_items
        ):
            self.__favorite_items.append(item)

    def remove_favorite_item(self, item):
        if not isinstance(item, OrderItem):
            raise TypeError("Favorite item must be an OrderItem")

        self.__favorite_items = [
            favorite
            for favorite in self.__favorite_items
            if favorite.name != item.name
        ]

    def take_gift(self, gift):
        # Any object that provides open_gift() is accepted.
        if not isinstance(gift, GiftInterface):
            raise TypeError("Gift must have an open_gift() method")

        self.__gift = gift

    def open_gift(self):
        if self.__gift is None:
            print("No gift available")
            return

        self.__gift.open_gift()

    def __repr__(self):
        return (
            f"Customer(id={self.__id}, "
            f"name='{self.__first_name} {self.__last_name}', "
            f"type={self.__customer_type.value})"
        )
