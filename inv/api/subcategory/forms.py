from django import forms
from .models import SubCategory

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter subcategory name',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
        }
        labels = {
            'name': 'Subcategory Name',
            'category': 'Parent Category',
        }
        help_texts = {
            'name': 'Enter a unique subcategory name.',
            'category': 'Select the parent category this subcategory belongs to.',
        }
        error_messages = {
            'name': {
                'unique_together': "This subcategory already exists under the selected category.",
            },
        }