
import unittest

from models.customer import Customer, CustomerType
from models.order_item import OrderItem
from models.order import Order, VIPOrder, PaymentType
from models.gift import Gift


class TestOrderSystem(unittest.TestCase):

    def setUp(self):
        # Reset IDs so each test is independent.
        Customer._used_ids.clear()
        Order._used_ids.clear()

        self.regular = Customer(
            1, "Alex", "Smith",
            "alex@example.com", "Tel Aviv"
        )

        self.vip = Customer(
            2, "Oleg", "Byashimov",
            "oleg@example.com", "Lod",
            CustomerType.VIP, 15
        )

        self.laptop = OrderItem(1, "Laptop", 3500)
        self.mouse = OrderItem(2, "Mouse", 150)

    def test_regular_order_total(self):
        order = Order(
            101, "Regular Purchase", "Tel Aviv",
            [self.laptop, self.mouse],
            self.regular, PaymentType.CASH
        )

        self.assertEqual(order.total_price, 3650)

    def test_vip_order_discount(self):
        order = VIPOrder(
            102, "VIP Purchase", "Lod",
            [self.laptop, self.mouse],
            self.vip, PaymentType.CREDIT_CARD
        )

        self.assertAlmostEqual(order.total_price, 3102.5)

    def test_duplicate_customer_id(self):
        with self.assertRaises(ValueError):
            Customer(
                1, "Another", "Customer",
                "another@example.com", "Haifa"
            )

    def test_duplicate_order_id(self):
        Order(
            101, "First", "Tel Aviv",
            [self.laptop],
            self.regular, PaymentType.CASH
        )

        with self.assertRaises(ValueError):
            Order(
                101, "Second", "Lod",
                [self.mouse],
                self.vip, PaymentType.CASH
            )

    def test_duplicate_item_id_in_order(self):
        duplicate = OrderItem(1, "Keyboard", 300)

        with self.assertRaises(ValueError):
            Order(
                101, "Invalid Order", "Tel Aviv",
                [self.laptop, duplicate],
                self.regular, PaymentType.CASH
            )

    def test_regular_customer_cannot_make_vip_order(self):
        with self.assertRaises(ValueError):
            VIPOrder(
                101, "Invalid VIP", "Tel Aviv",
                [self.laptop],
                self.regular, PaymentType.CASH
            )

    def test_favorites_deduplicated_by_name(self):
        another_laptop = OrderItem(99, "Laptop", 4000)

        Order(
            101, "First", "Tel Aviv",
            [self.laptop],
            self.regular, PaymentType.CASH
        )

        Order(
            102, "Second", "Tel Aviv",
            [another_laptop],
            self.regular, PaymentType.CASH
        )

        self.assertEqual(len(self.regular.favorite_items), 1)

    def test_remove_favorite(self):
        self.regular.add_favorite_item(self.laptop)
        self.regular.remove_favorite_item(self.laptop)

        self.assertEqual(self.regular.favorite_items, [])

    def test_gift(self):
        gift = Gift("Headset")
        self.vip.take_gift(gift)

        self.assertIs(self.vip.gift, gift)

    def test_negative_item_price(self):
        with self.assertRaises(ValueError):
            OrderItem(3, "Invalid", -100)


if __name__ == "__main__":
    unittest.main()
