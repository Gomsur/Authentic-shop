from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('subscribers/', views.SubscriberListView.as_view(), name='subscriber_list'),
    path('subscriber/<int:pk>/', views.SubscriberDetailView.as_view(), name='subscriber_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
]
