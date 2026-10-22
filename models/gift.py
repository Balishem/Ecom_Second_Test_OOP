from abc import ABC, abstractmethod


class GiftInterface(ABC):
    """A customer gift can be of any type, but must have open_gift().

    Classes inherit from this interface explicitly, but any object that
    simply defines a callable open_gift() is also treated as a gift.
    """

    @abstractmethod
    def open_gift(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is GiftInterface:
            if callable(getattr(subclass, "open_gift", None)):
                return True
        return NotImplemented


class Gift(GiftInterface):
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def open_gift(self):
        print("Congratulations! you got a new gift! Enjoy!")

    def __repr__(self):
        return f"Gift(name={self.__name!r})"
