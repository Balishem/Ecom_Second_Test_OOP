
import contextlib
import io
import unittest

from models.customer import Customer, CustomerType
from models.order_item import OrderItem
from models.order import Order, VIPOrder, PaymentType
from models.gift import Gift, GiftInterface


class TestOrderSystem(unittest.TestCase):

    def setUp(self):
        # Reset IDs so each test is independent.
        Customer.reset_ids()
        Order.reset_ids()

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

    def test_open_gift_prints_message(self):
        buffer = io.StringIO()
        self.vip.take_gift(Gift("Headset"))

        with contextlib.redirect_stdout(buffer):
            self.vip.open_gift()

        self.assertEqual(
            buffer.getvalue().strip(),
            "Congratulations! you got a new gift! Enjoy!"
        )

    def test_open_gift_without_gift(self):
        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer):
            self.regular.open_gift()

        self.assertEqual(buffer.getvalue().strip(), "No gift available")

    def test_gift_can_be_any_type_with_open_gift(self):
        class CustomGift:
            def open_gift(self):
                print("custom")

        self.regular.take_gift(CustomGift())
        self.assertIsInstance(self.regular.gift, GiftInterface)

    def test_gift_without_open_gift_rejected(self):
        with self.assertRaises(TypeError):
            self.regular.take_gift("not a gift")

    def test_vip_customer_without_discount(self):
        no_discount = Customer(
            3, "Dana", "Levi", "dana@example.com", "Haifa",
            CustomerType.VIP
        )
        order = VIPOrder(
            103, "VIP No Discount", "Haifa",
            [self.laptop],
            no_discount, PaymentType.CASH
        )

        self.assertEqual(order.total_price, 3500)

    def test_regular_customer_may_have_discount_but_not_applied(self):
        customer = Customer(
            4, "Noa", "Cohen", "noa@example.com", "Lod",
            CustomerType.REGULAR, 10
        )
        order = Order(
            104, "Regular", "Lod",
            [self.laptop],
            customer, PaymentType.CASH
        )

        self.assertEqual(order.total_price, 3500)

    def test_vip_total_is_rounded_to_two_decimals(self):
        customer = Customer(
            5, "Ron", "Bar", "ron@example.com", "Lod",
            CustomerType.VIP, 33
        )
        order = VIPOrder(
            105, "Rounded", "Lod",
            [OrderItem(10, "Cable", 10.01)],
            customer, PaymentType.CHECK
        )

        self.assertEqual(order.total_price, 6.71)

    def test_negative_item_price(self):
        with self.assertRaises(ValueError):
            OrderItem(3, "Invalid", -100)


if __name__ == "__main__":
    unittest.main()
