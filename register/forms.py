from django import forms
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    professionalink = forms.URLField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("User with that email already exists!")
        return email