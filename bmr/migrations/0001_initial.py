# Generated by Django 3.2.9 on 2021-11-27 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default='', max_length=20)),
                ('calories', models.IntegerField(default=0)),
                ('meal_type', models.CharField(default='extras', max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='BMRDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], default='m', max_length=1)),
                ('weight', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('age', models.IntegerField(default=0)),
                ('life_style', models.IntegerField(choices=[(1, 'sedentary'), (2, 'lightly active'), (3, 'moderately active'), (4, 'very active'), (5, 'extra active')], default=0)),
                ('bmr', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
