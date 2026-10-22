
from bonus.animals import Animal, Pet, Spider, Cat, Fish


def main():
    spider = Spider()
    cat = Cat("Tom")
    cat_without_name = Cat()
    fish = Fish()

    print("=== SPIDER ===")
    spider.walk()
    spider.eat()

    print("\n=== CAT ===")
    print("Name:", cat.getName())
    cat.walk()
    cat.play()
    cat.eat()

    print("\n=== CAT WITHOUT NAME ===")
    cat_without_name.setName("Garfield")
    print("Name:", cat_without_name.getName())

    print("\n=== FISH ===")
    fish.setName("Nemo")
    print("Name:", fish.getName())
    fish.walk()
    fish.play()
    fish.eat()

    print("\n=== INHERITANCE CHECK ===")
    print(isinstance(spider, Animal))
    print(isinstance(cat, Pet))
    print(isinstance(fish, Animal))


if __name__ == "__main__":
    main()
