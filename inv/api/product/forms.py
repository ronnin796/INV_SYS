from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from api.suppliers.models import Supplier
from api.category.models import Category
from api.subcategory.models import SubCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'subcategory', 'supplier']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter product name',
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter product price',
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'subcategory': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'supplier': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Start with empty subcategory queryset
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            # POST or GET request with category selected
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    category_id=category_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            # Editing an existing product
            self.fields['subcategory'].queryset = SubCategory.objects.filter(
                category=self.instance.category
            ).order_by('name')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A product with this name already exists.")
        return name
