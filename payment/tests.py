from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import BillingAddress

User = get_user_model()

class BillingAddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects._create_user(email='test@example.com', password='password')
        cls.billing_address = BillingAddress.objects.create(
            user=cls.user,
            address='123 Test Street',
            zipcode='12345',
            city='Test City',
            country='Test Country'
        )

    def test_billing_address_creation(self):
        billing_address = BillingAddress.objects.get(id=self.billing_address.id)
        self.assertEqual(billing_address.user, self.user)
        self.assertEqual(billing_address.address, '123 Test Street')
        self.assertEqual(billing_address.zipcode, '12345')
        self.assertEqual(billing_address.city, 'Test City')
        self.assertEqual(billing_address.country, 'Test Country')

    def test_is_fully_filled(self):
        billing_address = BillingAddress.objects.get(id=self.billing_address.id)
        self.assertTrue(billing_address.is_fully_filled())

    def test_is_not_fully_filled(self):
        billing_address = BillingAddress.objects.create(user=self.user, address='', zipcode='', city='', country='')
        self.assertFalse(billing_address.is_fully_filled())
