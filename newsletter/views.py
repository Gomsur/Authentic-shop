from django.shortcuts import render, redirect
from .forms import SubscriberForm
from django.contrib import messages

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to our newsletter.')
            return redirect('shop:home')  # Redirect to home or any other page
    else:
        form = SubscriberForm()
    return render(request, 'newsletter/subscribe.html', {'form': form})


def about(request):
    return render(request, 'newsletter/about.html')
