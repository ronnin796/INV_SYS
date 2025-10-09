from django import forms
from .models import Supplier
from django.core.exceptions import ValidationError

from django import forms
from .models import Supplier
from django.core.exceptions import ValidationError

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_email', 'phone_number', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter supplier name',
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'contact_email': forms.EmailInput(attrs={
                'placeholder': 'Enter contact email',
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter phone number',
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Enter address',
                'class': 'w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

    def clean_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        if Supplier.objects.filter(contact_email=email).exists():
            raise ValidationError("A supplier with this email already exists.")
        return email
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if Supplier.objects.filter(phone_number=phone).exists():
            raise ValidationError("A supplier with this phone number already exists.")
        return phone