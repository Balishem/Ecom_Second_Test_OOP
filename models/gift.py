
class Gift:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def open_gift(self):
        print("Congratulations! you got a new gift! Enjoy!")

    def __repr__(self):
        return f"Gift(name={self.__name!r})"
