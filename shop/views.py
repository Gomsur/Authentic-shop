from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView

from . models import Product, Category, Review

from .forms import ProductForm, CategoryForm

from django.core.paginator import Paginator


class Home(ListView):
    model = Product
    template_name = 'shop/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['meta_title'] = "Welcome to Authentic Shop"
        context['meta_description'] = "Browse our wide range of high-quality products and enjoy a seamless shopping experience."
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['meta_title'] = product.name
        context['meta_description'] = product.preview_text
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['products'] = category.category.all()  # Second category is the related name in the Product model
        return context


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    existing_review = Review.objects.filter(user=request.user, product=product).exists()
    if existing_review:
        messages.error(request, "You have already reviewed this product.")
        return redirect('shop:product_detail', pk=pk)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        
        messages.success(request, "Thank you for your review!")
        return redirect('shop:product_detail', pk=pk)

    return render(request, 'shop/add_review.html', {'product': product})

def error_404_view(request, exception):
    return render(request, '404.html', status=404)



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('shop:home')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form, 'meta_title': "Add New Product", 'meta_description': "Add a new product to the store."})

def product_list(request):
    products = Product.objects.all()

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'meta_title': "Product List",
        'meta_description': "Browse through our list of products."
    }
    return render(request, 'shop/product_list.html', context)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('shop:home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('shop:home')


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('shop:home')
    else:
        form = CategoryForm()
    return render(request, 'shop/add_category.html', {'form': form})