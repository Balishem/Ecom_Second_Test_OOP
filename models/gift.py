
class Gift:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def open_gift(self):
        print("Congratulations epta! you got a new gift! Enjoy! Before opening drink some Vodka and say hello to Bibi")

    def __repr__(self):
        return f"Gift(name={self.__name!r})"
