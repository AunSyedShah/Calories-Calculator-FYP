# Generated by Django 4.0 on 2022-01-06 14:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bmr', '0013_alter_fooditem_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]