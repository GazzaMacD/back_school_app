# Generated by Django 4.2.1 on 2023-09-27 04:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("addresses", "0006_alter_contactaddress_contact_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="is_learning_center",
            field=models.BooleanField(default=False, verbose_name="Is Learning Center"),
        ),
    ]
