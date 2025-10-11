from django import forms
from .models import Warehouse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'manager', 'contact_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter warehouse name',
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter location',
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'manager': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
            'contact_number': forms.TextInput(attrs={
                'placeholder': 'Enter contact number (optional)',
                'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show staff or admin users as potential warehouse managers
        self.fields['manager'].queryset = User.objects.filter(is_approved=True)
        self.fields['manager'].required = False  # Make manager optional