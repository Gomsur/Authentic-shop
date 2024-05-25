from django.shortcuts import render, redirect
from .forms import SubscriberForm
from django.contrib import messages

from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings

from django.views.generic import ListView, DetailView
from .models import Subscriber

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to our newsletter.')
            return redirect('shop:home')
    else:
        form = SubscriberForm()
    return render(request, 'newsletter/subscribe.html', {'form': form})


def about(request):
    return render(request, 'newsletter/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Email subject and message
        subject = f"Contact Form Submission from {name} {surname}"
        message_body = render_to_string('newsletter/email/contact_email.html', {
            'name': name,
            'surname': surname,
            'email': email,
            'phone': phone,
            'message': message
        })
        
        # Send email
        email_message = EmailMessage(subject, message_body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
        email_message.reply_to = [email]
        email_message.content_subtype = 'html'
        email_message.send()
        
        return redirect('newsletter:contact_success')
    return render(request, 'newsletter/contact.html')

def contact_success(request):
    return render(request, 'newsletter/contact_success.html')



class SubscriberListView(ListView):
    model = Subscriber
    template_name = 'newsletter/subscriber_list.html'
    context_object_name = 'subscribers'


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = 'newsletter/subscriber_detail.html'
    context_object_name = 'subscriber'
