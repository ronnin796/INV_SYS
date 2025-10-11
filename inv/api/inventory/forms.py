# inventory/forms.py
from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['warehouse', 'product', 'quantity', 'reorder_level']
        widgets = {
            'warehouse': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'product': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'placeholder': 'Enter quantity'
            }),
            'reorder_level': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none',
                'placeholder': 'Enter reorder threshold'
            }),
        }
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity
    def clean_reorder_level(self):
        reorder_level = self.cleaned_data.get('reorder_level')
        if reorder_level < 0:
            raise forms.ValidationError("Reorder level cannot be negative.")
        return reorder_level
    def clean(self):
        cleaned_data = super().clean()
        warehouse = cleaned_data.get('warehouse')
        product = cleaned_data.get('product')

        if warehouse and product:
            qs = Inventory.objects.filter(warehouse=warehouse, product=product)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This product already exists in the selected warehouse.")

        return cleaned_data

    