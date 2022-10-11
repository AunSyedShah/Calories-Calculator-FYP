from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from .models import BMRDetail, FoodItem


class BMRForm(ModelForm):
    class Meta:
        model = BMRDetail
        fields = ('gender', 'weight', 'height', 'age', 'life_style',)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
        # add placeholders to the form fields
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        widgets = {
            'date_added': DateInput()
        }
        fields = ("item_name", "calories", "meal_type", "date_added")
