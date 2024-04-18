from django.urls import path
from .import views
app_name = 'payment'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_view, name='orders'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),

    # Stripe Payment Gateway
    path('payment/stripe/', views.paymentStripe, name='payment_stripe'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
]