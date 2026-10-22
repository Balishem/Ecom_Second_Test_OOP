
class OrderItem:
    def __init__(self, item_id: int, name: str, price: float):
        if not isinstance(item_id, int) or isinstance(item_id, bool):
            raise TypeError("Item ID must be an integer")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Item name cannot be empty")

        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError("Item price must be a number")

        if price < 0:
            raise ValueError("Item price cannot be negative")

        self.__id = item_id
        self.__name = name
        self.__price = price

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    def __repr__(self):
        return (
            f"OrderItem(id={self.__id}, "
            f"name={self.__name!r}, price={self.__price})"
        )
