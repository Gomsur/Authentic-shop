from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from .models import Cart, Order
from shop.models import Product

from django.contrib import messages


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)

    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        
        if order.orderItems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated")
            return redirect('shop:home')
        else:
            order.orderItems.add(order_item[0])
            messages.info(request, "This item was added to your cart.")
            return redirect('shop:home')
    
    else:
        order = Order(user=request.user)
        order.save()
        order.orderItems.add(order_item[0])
        messages.info(request, "This item was added to your cart.")
        return redirect('shop:home')




@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'order/cart.html', context={'carts': carts, 'order': order})
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect('shop:home')



@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            order.orderItems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your cart.")
            return redirect("order:cart")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("shop:home")


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated.")
                return redirect("order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart.")
            return redirect("shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("shop:home")



@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated.")
                return redirect("order:cart")
            else:
                order.orderItems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart.")
                return redirect("order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart.")
            return redirect("shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("shop:home")