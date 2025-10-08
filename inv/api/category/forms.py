from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter category name',
            }),
        }
        labels = {
            'name': 'Category Name',
        }
        help_texts = {
            'name': 'Enter a unique category name.',
        }