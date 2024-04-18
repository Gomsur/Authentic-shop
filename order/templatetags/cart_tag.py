from atexit import register
from django import template
from order.models import Order

register = template.Library()


@register.filter
def cart_total(user):  # It will take a parameter as user.
    order = Order.objects.filter(user=user, ordered=False)  # It will check the orders without payment for this user.
    
    if order.exists():
        return order[0].orderItems.count()  # To convert the order from tuple/list to single object we use [0].
    else:
        return 0
