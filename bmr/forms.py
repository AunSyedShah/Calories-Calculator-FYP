from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import BMRDetail, FoodItem


class BMRForm(ModelForm):
    class Meta:
        model = BMRDetail
        fields = ('gender', 'weight', 'height', 'age', 'life_style',)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")


class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        fields = ("item_name", "calories", "meal_type")
