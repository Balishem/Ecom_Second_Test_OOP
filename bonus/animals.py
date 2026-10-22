
from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, legs: int):
        self._legs = legs

    @property
    def legs(self):
        return self._legs

    def walk(self):
        print(f"This animal walks on {self._legs} legs.")

    @abstractmethod
    def eat(self):
        pass


class Pet(ABC):
    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def setName(self, name: str):
        pass

    @abstractmethod
    def play(self):
        pass


class Spider(Animal):
    def __init__(self):
        super().__init__(8)

    def eat(self):
        print("Spider eats insects.")


class Cat(Animal, Pet):
    def __init__(self, name: str = ""):
        super().__init__(4)
        self._name = name

    def getName(self) -> str:
        return self._name

    def setName(self, name: str):
        self._name = name

    def play(self):
        print(f"{self._name or 'Cat'} is playing.")

    def eat(self):
        print("Cat eats fish.")


class Fish(Animal, Pet):
    def __init__(self):
        super().__init__(0)
        self._name = ""

    def getName(self) -> str:
        return self._name

    def setName(self, name: str):
        self._name = name

    def play(self):
        print(f"{self._name or 'Fish'} is playing.")

    def walk(self):
        print("Fish cannot walk. It swims.")

    def eat(self):
        print("Fish eats fish food.")
