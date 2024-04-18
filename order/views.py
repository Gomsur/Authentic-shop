from django.shortcuts import render, get_object_or_404, redirect

# Authentications
from django.contrib.auth.decorators import login_required

# Model
from .models import Cart, Order
from shop.models import Product

# Messages
from django.contrib import messages

# Create your views here.

@login_required
def add_to_cart(request, pk):  # Primary Key(pk) of the item which one we want to add to the cart.
    item = get_object_or_404(Product, pk=pk)  # It will call the item which one we want to add to the cart.
    # print("Item:")
    # print(item)
    '''
        It will check that the item is already in the cart or not.
        get_or_create means if the item is in cart then call it. If the item is brand new then create it(add to the cart) according to logged in user and purchased=False.
    '''
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)  # purchased=False means they are in the cart. if purchased=True then we will not call them.
    # print("Order Item Object:")
    # print(order_item)
    # print(order_item[0])
    '''
        Check the item is in my order or not which one we added.
        We will check if the item I added is in my order or not.
        Check if the current user has any active order. ordered=False means Not Paid(Incomplete order). ordered=True means Paid
    '''
    order_qs = Order.objects.filter(user=request.user, ordered=False)  # ordered=False means we didn't ordered it or paid for it. If ordered=True means we paid for it.
    # print("Order Qs:")
    # print(order_qs)
    # Check if the current user has any Incomplete/Inactive order.
    if order_qs.exists():
        order = order_qs[0]  # Index 0. First object. By indexing we are converting the tuple into object.
        # print("If Order Exist:")
        # print(order)
        # If the item I added is in my order items. We will add the same item.
        if order.orderItems.filter(item=item).exists():  # It will check that we have already ordered the item or not  which one we want to add now.
            order_item[0].quantity += 1  # By indexing we are converting the tuple into object.
            order_item[0].save()
            messages.info(request, "This item quantity was updated") # Suppose the item is already in the cart then it will increase the quantity of that item.
            return redirect('shop:home')
        # If the item I added is not in my order items
        else:
            order.orderItems.add(order_item[0])  # Add the new item to my cart.
            messages.info(request, "This item was added to your cart.")
            return redirect('shop:home')
    
    # There is no Incomplete/Inactive order. User didn't add any item to the cart, didn't ordered anything.
    else:
        order = Order(user=request.user)  # Create new order
        order.save()  # Save new order
        order.orderItems.add(order_item[0])  # Add the item to the cart which one selected.
        messages.info(request, "This item was added to your cart.")
        return redirect('shop:home')




@login_required
def cart_view(request):
    # If any item in the carts that means the item will be in orders also.
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)  # Orders will bind all the objects/items for specific user.
    if carts.exists() and orders.exists():
        order = orders[0] # Orders are in tuple So we need to convert into a single object. If not then we can't visit the order items or attributes.
        return render(request, 'order/cart.html', context={'carts': carts, 'order': order})
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect('shop:home')



@login_required
def remove_from_cart(request, pk):  # pk of that item which we want to delete.
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)   # Order check. It will check that user have any order or not.

    if order_qs.exists():  # If it's True that means it has orders.
        order = order_qs[0]  # Convert into a single object.
        if order.orderItems.filter(item=item).exists():  # Checking that Among the orderItems in my order, does the item I want to remove exist?
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)  # Finding the item from orderItems to delete.
            order_item = order_item[0]
            order.orderItems.remove(order_item)  # It will delete items from order table.
            order_item.delete()  # It will delete item from cart.
            messages.warning(request, "This item was removed from your cart.")
            return redirect("order:cart")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("shop:home")

    else: # If it's False that means it has no order. So, there is no item in the cart.
        messages.info(request, "You don't have an active order")
        return redirect("shop:home")


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)  # Call the item which we want to increase.
    order_qs = Order.objects.filter(user=request.user, ordered=False)   # Check that user have any active order or not.
    
    if order_qs.exists(): # If it's True
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():  # Checking that Among the orderItems in my order, does the item I want to increase exist?
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)  # Finding the item from orderItems to increase.
            order_item = order_item[0] # Indexing
            # Increase the item if it's equal or more than 1.
            if order_item.quantity >= 1:
                order_item.quantity += 1  # Increase 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated.")
                return redirect("order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart.")
            return redirect("shop:home")
    else:   # If it's not True that means i/user don't have any order.
        messages.info(request, "You don't have an active order")
        return redirect("shop:home")



@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)  # Call the item which we want to decrease.
    order_qs = Order.objects.filter(user=request.user, ordered=False)   # Check that user have any active order or not.
    
    if order_qs.exists(): # If it's True that means it has order.
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():  # Checking that Among the orderItems in my order, does the item I want to decrease exist?
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)  # Finding the item from orderItems to decrease.
            order_item = order_item[0] # Indexing
            # Decrease the item if it's more than 1.
            if order_item.quantity > 1:
                order_item.quantity -= 1  # Decrease 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated.")
                return redirect("order:cart")
            else:  # If quantity is 1, So nothing to decrease. We will remove that.
                order.orderItems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart.")
                return redirect("order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart.")
            return redirect("shop:home")
    else:   # If it's False that means i/user don't have any order.
        messages.info(request, "You don't have an active order")
        return redirect("shop:home")