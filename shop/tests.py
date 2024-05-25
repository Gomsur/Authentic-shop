from django.test import TestCase
from shop.models import Category, Product, Review

from django.contrib.auth import get_user_model


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(title="Test Category")
        self.assertEqual(category.title, "Test Category")

class ProductModelTest(TestCase):
    def test_product_creation(self):
        category = Category.objects.create(title="Test Category")
        product = Product.objects.create(
            mainImage="path/to/image.jpg",
            name="Test Product",
            category=category,
            preview_text="Test preview text",
            detail_text="Test detail text",
            price=10.0
        )
        self.assertEqual(product.name, "Test Product")

class ReviewModelTest(TestCase):
    def test_review_creation(self):
        category = Category.objects.create(title="Test Category")
        product = Product.objects.create(
            mainImage="path/to/image.jpg",
            name="Test Product",
            category=category,
            preview_text="Test preview text",
            detail_text="Test detail text",
            price=10.0
        )

        User = get_user_model()
        user = User.objects._create_user(email="testuser@example.com", password="password")

        review = Review.objects.create(
            product=product,
            user=user,
            rating=4,
            comment="Test comment"
        )
        self.assertEqual(review.rating, 4)