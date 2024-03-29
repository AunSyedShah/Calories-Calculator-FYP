from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BMRDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female")
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="m")
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    LIFE_STYLE_CHOICES = (
        (1, "sedentary"),
        (2, "lightly active"),
        (3, "moderately active"),
        (4, "very active"),
        (5, "extra active"),
    )
    life_style = models.IntegerField(choices=LIFE_STYLE_CHOICES, default=0)
    bmr = models.IntegerField(default=0)
    user_profile_pic = models.ImageField(upload_to='profile_pics', blank=True)


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
    meal_type = models.CharField(choices=MEAL_TYPE_CHOICE, max_length=9, default="extras")
    date_added = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.item_name
