from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from shop.models import Product, Category
from accounts.models import User
from order.models import Order
from payment.models import BillingAddress
from newsletter.models import Subscriber

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'shop:home', 
            'newsletter:about', 
            'newsletter:contact',
            'accounts:signup',
            'accounts:login',
            'accounts:logout',
            'accounts:profile',
            'order:cart',
            'payment:checkout',
            'payment:orders'
        ]

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created
    
    def location(self, obj):
        return reverse('shop:product_detail', args=[obj.pk])
    


class CategorySitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('shop:category_detail', args=[obj.pk])

class UserSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return User.objects.all()

    def location(self, obj):
        return reverse('accounts:profile')

class OrderSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Order.objects.all()

    def location(self, obj):
        return reverse('order:cart')

class BillingAddressSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return BillingAddress.objects.all()

    def location(self, obj):
        return reverse('payment:orders')
    

class SubscriberSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Subscriber.objects.all()

    def location(self, obj):
        return reverse('newsletter:subscriber_detail', args=[obj.pk])


sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'users': UserSitemap,
    'orders': OrderSitemap,
    'billing_addresses': BillingAddressSitemap,
    'subscribers': SubscriberSitemap,
}