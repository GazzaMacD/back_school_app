# Generated by Django 4.2.1 on 2023-08-08 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="address",
            name="modified",
            field=models.DateTimeField(auto_now=True, verbose_name="modified"),
        ),
    ]
