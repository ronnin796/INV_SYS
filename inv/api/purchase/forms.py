from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, PurchaseItem
from api.product.models import Product

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ["supplier", "warehouse", "reference_number", "status"]
        widgets = {
            "supplier": forms.Select(attrs={"class": "w-full ..."}),
            "warehouse": forms.Select(attrs={"class": "w-full ..."}),
            "reference_number": forms.TextInput(attrs={"class": "w-full ..."}),
            "status": forms.Select(attrs={"class": "w-full ..."}),
        }


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "price"]
        widgets = {
            "product": forms.Select(attrs={"class": "w-full ... product-select"}),
            "quantity": forms.NumberInput(attrs={"class": "w-full ... qty-input", "step": "1"}),
            "price": forms.NumberInput(attrs={"class": "w-full ... price-input", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        supplier_id = kwargs.pop("supplier_id", None)
        super().__init__(*args, **kwargs)
        # If editing an existing item, product field should include selected product
        if self.instance and self.instance.pk:
            # include that product plus supplier's products
            if self.instance.product:
                self.fields["product"].queryset = Product.objects.filter(
                    pk=self.instance.product.pk
                ) | Product.objects.filter(supplier_id=supplier_id)
        else:
            if supplier_id:
                self.fields["product"].queryset = Product.objects.filter(supplier_id=supplier_id)
            else:
                self.fields["product"].queryset = Product.objects.none()

    def clean_price(self):
        price = self.cleaned_data.get("price")
        product = self.cleaned_data.get("product")
        if (price in [None, ""] or price == 0) and product:
            # fallback to product price if provided
            return getattr(product, "price", 0)
        return price


PurchaseItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseItem,
    form=PurchaseItemForm,
    extra=1,
    can_delete=True,
)
