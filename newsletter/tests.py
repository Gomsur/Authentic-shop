from django.test import TestCase
from django.db.utils import IntegrityError
from .models import Subscriber


class SubscriberModelTest(TestCase):
    def test_create_subscriber(self):
        email = "test@example.com"
        subscriber = Subscriber.objects.create(email=email)

        self.assertIsNotNone(subscriber)
        self.assertEqual(subscriber.email, email)

    def test_unique_email(self):
        email = "test@example.com"
        Subscriber.objects.create(email=email)

        with self.assertRaises(IntegrityError):
            Subscriber.objects.create(email=email)
