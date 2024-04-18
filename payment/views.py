from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from order.models import Order, Cart
from .models import BillingAddress
from .forms import BillingAddressForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .utils import send_payment_confirmation_email
import stripe
from django.conf import settings
from django.utils.crypto import get_random_string

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    saved_address, _ = BillingAddress.objects.get_or_create(user=request.user)
    form = BillingAddressForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingAddressForm(instance=saved_address)
            messages.success(request, 'Shipping Address Saved!')
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderItems.all()
    order_total = order_qs[0].get_totals()
    
    return render(request, 'payment/checkout.html', context={'form': form, 'order_items': order_items, 'order_total': order_total, 'saved_address': saved_address})

@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {'orders': orders}
    except:
        messages.warning(request, 'You do not have an active order!')
        return redirect('shop:home')
    return render(request, 'payment/order.html', context)

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.orderItems.all()
    
    for item in items:
        reviews = item.item.reviews.all()
        item.reviews = reviews
        item.already_reviewed = reviews.filter(user=request.user).exists()
    
    return render(request, 'payment/order_details.html', {'order': order, 'items': items})

@login_required
def paymentStripe(request):
    key = settings.STRIPE_PUBLIC_KEY
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs.first()
    
    if not order:
        messages.error(request, 'You do not have an active order.')
        return redirect('shop:home')
    
    order_total = order.get_totals()
    total = int(order_total * 100)
    
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=total,
                currency='usd',
                description='Payment for Order',
                source=token,
            )
            if charge.status == "succeeded":
                orderId = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                order.ordered = True
                order.paymentId = charge.id
                order.orderId = f'#{orderId}'  # Generating and assigning order ID
                order.save()
                
                cartItems = Cart.objects.filter(user=request.user)
                for item in cartItems:
                    item.purchased = True
                    item.save()
                
                send_payment_confirmation_email(request.user.email, order.id)
                return redirect('payment:payment_success', order_id=order.id)
            else:
                messages.error(request, 'Payment failed. Please try again or contact support.')
                return redirect('payment:payment_failure')
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
            messages.error(request, f"Payment failed: {err['message']}")
            return redirect('payment:payment_failure')

    return render(request, 'payment/payment_stripe.html', {"key": key, "total": total, "order": order})



def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment/payment_success.html', {'order': order})

def payment_failure(request):
    return render(request, 'payment/payment_failure.html')
