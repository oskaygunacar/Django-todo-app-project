from django import forms
from django.contrib.auth.models import User
from .models import Todo, Profile, Category
from django.core import validators
from tinymce.widgets import TinyMCE
import json

def validate_email_unique(value):
    if User.objects.filter(email=value).exists():
        raise forms.ValidationError("This Email is already registered. Please use different email. ")


class UserForm(forms.ModelForm):
    email = forms.EmailField(validators=[validators.EmailValidator(message='Please check your email format.'), validate_email_unique])
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validators.MinLengthValidator(10, message='You need to write a minimum 10 character long password'),])

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username", # Django automatically validate uniqueness of usernames in database
            "email",
            "password",
        ]

class ProfileModelForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'description',
        ]

class TodoModelForm(forms.ModelForm):

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 20}))
    tag = forms.CharField(required=False)

    class Meta:
        model = Todo
        fields = [
            'title',
            'is_active',
            'category',
            'content',
            'tag',
        ]


class CategoryModelForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'title',
            'is_active',
        ]