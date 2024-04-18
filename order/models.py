from venv import create
from django.db import models

from django.conf import settings

# Model
from shop.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)   # Which item added to the cart.
    quantity = models.IntegerField(default=1)  # How many we ordered.
    purchased = models.BooleanField(default=False)   # If we purchased the cart items(Value will be True), it won't show on cart anymore. Because i paid for this.
    created = models.DateTimeField(auto_now_add=True)  # It will add once when we add item.
    updated = models.DateTimeField(auto_now=True)   # It will update every time when we updated the cart or item. 

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    # Total price of an Individual item (Price of item * quantity of item)
    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')  # Will show 2 digits after dot.
        return float_total


class Order(models.Model):
    orderItems = models.ManyToManyField(Cart)   # One item in a cart can be in multiple orders and An order can contain many cart items.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)   # Already ordered or not. If we paid for it then it will be True.
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)    # We can call it transaction id.
    orderId = models.CharField(max_length=200, blank=True, null=True)

    # Total price of all the products/items
    def get_totals(self):
        total = 0
        for order_item in self.orderItems.all():
            total += float(order_item.get_total())  # Call the get_total function.
        return total
    