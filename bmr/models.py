from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BMRDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    GENDER_CHOICES = (
        ("m", "male"),
        ("f", "female")
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="m")
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    age = models.IntegerField(default=0)
    LIFE_STYLE_CHOICES = (
        (1, "sedentary"),
        (2, "lightly active"),
        (3, "moderately active"),
        (4, "very active"),
        (5, "extra active"),
    )
    life_style = models.IntegerField(choices=LIFE_STYLE_CHOICES, default=0)
    bmr = models.FloatField(default=0)


class FoodItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item_name = models.CharField(max_length=20, default="")
    calories = models.IntegerField(default=0)
    MEAL_TYPE_CHOICE = (
        ("breakfast", "breakfast"),
        ("lunch", "lunch"),
        ("dinner", "dinner"),
        ("extras", "extras")
    )
    meal_type = models.CharField(max_length=9, default="extras")
