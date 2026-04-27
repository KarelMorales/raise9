from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    institution = forms.CharField(max_length=255, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Institution / Academe'}))
    position = forms.CharField(max_length=255, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Designation / Position'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'institution', 'position', 'password1', 'password2')