from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile

class ProfileModelTest(TestCase):
    def test_create_profile(self):
        user = get_user_model().objects.create(email='test@example.com', password='password')
        if not Profile.objects.filter(user=user).exists():
            profile = Profile.objects.create(user=user)
            self.assertEqual(profile.user.email, 'test@example.com')

    def test_is_fully_filled(self):
        user = get_user_model().objects.create(email='test@example.com', password='password')
        if not Profile.objects.filter(user=user).exists():
            profile = Profile.objects.create(user=user, username='test', full_name='Test User', address_1='123 Street',
                                             city='City', zipcode='12345', country='Country', phone='1234567890')
            self.assertTrue(profile.is_fully_filled())

class UserModelTest(TestCase):
    def test_create_user(self):
        user = get_user_model().objects._create_user(email='test@example.com', password='password')
        self.assertEqual(user.email, 'test@example.com')
