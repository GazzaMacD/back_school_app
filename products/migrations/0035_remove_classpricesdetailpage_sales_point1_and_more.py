# Generated by Django 4.2.1 on 2023-11-21 07:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0034_productservice_is_native_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="classpricesdetailpage",
            name="sales_point1",
        ),
        migrations.RemoveField(
            model_name="classpricesdetailpage",
            name="sales_point2",
        ),
    ]
