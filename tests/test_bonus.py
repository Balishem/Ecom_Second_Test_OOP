import unittest

from bonus.animals import Animal, Pet, Spider, Cat, Fish


class TestBonusAnimals(unittest.TestCase):

    def test_animal_is_abstract(self):
        with self.assertRaises(TypeError):
            Animal(4)

    def test_pet_is_abstract(self):
        with self.assertRaises(TypeError):
            Pet()

    def test_spider_is_animal_not_pet(self):
        spider = Spider()

        self.assertIsInstance(spider, Animal)
        self.assertNotIsInstance(spider, Pet)
        self.assertEqual(spider.legs, 8)

    def test_cat_constructors_and_name(self):
        named = Cat("Tom")
        unnamed = Cat()

        self.assertEqual(named.getName(), "Tom")
        self.assertEqual(unnamed.getName(), "")

        unnamed.setName("Garfield")
        self.assertEqual(unnamed.getName(), "Garfield")

    def test_cat_is_animal_and_pet(self):
        cat = Cat()

        self.assertIsInstance(cat, Animal)
        self.assertIsInstance(cat, Pet)

    def test_fish_is_animal_and_pet(self):
        fish = Fish()
        fish.setName("Nemo")

        self.assertIsInstance(fish, Animal)
        self.assertIsInstance(fish, Pet)
        self.assertEqual(fish.getName(), "Nemo")
        self.assertEqual(fish.legs, 0)

    def test_pet_name_must_be_string(self):
        with self.assertRaises(TypeError):
            Cat().setName(123)


if __name__ == "__main__":
    unittest.main()
