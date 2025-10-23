from django import forms
from django.forms import inlineformset_factory
from .models import SalesOrder, SalesItem
from api.product.models import Product

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ["customer", "warehouse", "reference_number", "status"]
        widgets = {
            "customer": forms.Select(attrs={"class": "w-full ..."}),
            "warehouse": forms.Select(attrs={"class": "w-full ..."}),
            "reference_number": forms.TextInput(attrs={"class": "w-full ..."}),
            "status": forms.Select(attrs={"class": "w-full ..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For new forms, prevent selecting "Completed" initially
        if not self.instance.pk:
            self.fields["status"].choices = [
                choice for choice in self.fields["status"].choices
                if choice[0] != "Completed"
            ]


class SalesItemForm(forms.ModelForm):
    class Meta:
        model = SalesItem
        fields = ["product", "quantity", "price"]
        widgets = {
            "product": forms.Select(attrs={"class": "w-full ... product-select"}),
            "quantity": forms.NumberInput(attrs={"class": "w-full ... quantity-input", "step": "1"}),
            "price": forms.NumberInput(attrs={"class": "w-full ... price-input", "step": "0.01"}),
            
            
        }

    def __init__(self, *args, **kwargs):
        warehouse_id = kwargs.pop("warehouse_id", None)
        super().__init__(*args, **kwargs)

        # If editing existing item, include its product and warehouse products
        if self.instance and self.instance.pk and self.instance.product:
            qs = Product.objects.filter(pk=self.instance.product.pk)
            if warehouse_id:
                qs |= Product.objects.filter(inventory_entries__warehouse_id=warehouse_id)
            self.fields["product"].queryset = qs.distinct()

            # Pre-fill price from product if not set
            if not self.initial.get("price"):
                self.initial["price"] = getattr(self.instance.product, "price", 0)

        # If new item, limit products to selected warehouse
        else:
            if warehouse_id:
                self.fields["product"].queryset = Product.objects.filter(
                    inventory_entries__warehouse_id=warehouse_id
                ).distinct()
            else:
                self.fields["product"].queryset = Product.objects.none()

    def clean_price(self):
        price = self.cleaned_data.get("price")
        product = self.cleaned_data.get("product")
        # fallback to product price if blank or 0
        if price in [None, ""] and product:
            return getattr(product, "price", 0)
        return price


# Create the inline formset
SalesItemFormSet = inlineformset_factory(
    SalesOrder,
    SalesItem,
    form=SalesItemForm,
    extra=1,
    can_delete=True,
)
