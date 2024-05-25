from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Product, Category
from order.models import Cart, Order

User = get_user_model()

class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects._create_user(email='testuser@example.com', password='password')
        cls.category = Category.objects.create(title='Test Category')
        cls.product = Product.objects.create(name='Test Product', price=10.0, category=cls.category)
        cls.cart_item = Cart.objects.create(user=cls.user, item=cls.product, quantity=2)

    def test_cart_item_creation(self):
        cart_item = Cart.objects.get(id=self.cart_item.id)
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.item, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertFalse(cart_item.purchased)

    def test_get_total(self):
        cart_item = Cart.objects.get(id=self.cart_item.id)
        total = cart_item.get_total()
        self.assertEqual(total, '20.00')


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects._create_user(email='testuser@example.com', password='password')
        cls.category = Category.objects.create(title='Test Category')
        cls.product = Product.objects.create(name='Test Product', price=10.0, category=cls.category)
        cls.cart_item = Cart.objects.create(user=cls.user, item=cls.product, quantity=2)
        cls.order = Order.objects.create(user=cls.user)
        cls.order.orderItems.add(cls.cart_item)

    def test_order_creation(self):
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.user, self.user)
        self.assertFalse(order.ordered)

    def test_get_totals(self):
        order = Order.objects.get(id=self.order.id)
        total = order.get_totals()
        self.assertEqual(total, 20.0)