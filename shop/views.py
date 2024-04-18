from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Import views
from django.views.generic import ListView, DetailView

# Models
from . models import Product, Category, Review


# Mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


# class Home(ListView):  # It will send object_list by default if we don't send anything with context dictionary.
#     model = Product
#     template_name = 'shop/home.html'
class Home(ListView):
    model = Product
    template_name = 'shop/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset



class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Check if the user has already reviewed this product
    existing_review = Review.objects.filter(user=request.user, product=product).exists()
    if existing_review:
        messages.error(request, "You have already reviewed this product.")
        return redirect('shop:product_detail', pk=pk)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Create the review
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        
        messages.success(request, "Thank you for your review!")
        return redirect('shop:product_detail', pk=pk)

    return render(request, 'shop/add_review.html', {'product': product})

def error_404_view(request, exception):
    return render(request, '404.html', status=404)