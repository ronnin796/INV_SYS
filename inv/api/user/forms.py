from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model


from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

User = get_user_model()  # this will be your CustomUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-4 rounded-xl border border-gray-300'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'class': 'w-full py-4 px-4 rounded-xl border border-gray-300'
    }))
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Invalid username or password")
        if not user.is_approved:
            raise ValidationError("Your account is awaiting admin approval.")
        cleaned_data["user"] = user
        return cleaned_data


class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-4 rounded-xl border border-gray-300'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-4 rounded-xl border border-gray-300'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'class': 'w-full py-4 px-4 rounded-xl border border-gray-300'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'w-full py-4 px-4 rounded-xl border border-gray-300'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')