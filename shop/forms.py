from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['mainImage', 'name', 'category', 'preview_text', 'detail_text', 'price', 'old_price']
        exclude = ['created']
        
        widgets = {
            'mainImage': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'preview_text': forms.Textarea(attrs={'class': 'form-control'}),
            'detail_text': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        # fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }