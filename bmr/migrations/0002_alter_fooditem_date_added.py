# Generated by Django 3.2.9 on 2022-03-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='date_added',
            field=models.DateField(blank=True, null=True),
        ),
    ]
