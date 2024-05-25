from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from order.models import Order

def send_payment_confirmation_email(user_email, order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Payment Confirmation'
    html_message = render_to_string('payment/email/payment_confirmation.html', {'user': user_email, 'order': order})
    plain_message = strip_tags(html_message)
    from_email = 'your_email@example.com'

    send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)
