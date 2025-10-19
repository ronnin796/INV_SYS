# inventory/forms.py
from django import forms
from .models import Inventory


from django import forms
from .models import Inventory
from api.suppliers.models import Supplier
from api.category.models import Category
from api.subcategory.models import SubCategory
from api.product.models import Product

class InventoryForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
        })
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
        })
    )

    class Meta:
        model = Inventory
        fields = ['warehouse', 'supplier', 'category', 'subcategory', 'product', 'quantity', 'reorder_level']
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'}),
            'product': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none','placeholder': 'Enter quantity'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none','placeholder': 'Enter reorder threshold'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate subcategories if category selected
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.product.subcategory:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.product.subcategory.category)

        # Dynamically filter products
        if 'subcategory' in self.data:
            try:
                subcat_id = int(self.data.get('subcategory'))
                self.fields['product'].queryset = Product.objects.filter(subcategory_id=subcat_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['product'].queryset = Product.objects.filter(subcategory=self.instance.product.subcategory)


    