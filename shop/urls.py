from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/<pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('product/<int:pk>/add_review/', views.add_review, name='add_review'),
]