# Generated by Django 3.2.9 on 2022-01-02 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bmr', '0005_alter_bmrdetail_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]