# Generated by Django 4.2.1 on 2023-11-15 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0030_productservice_class_quantity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productservice",
            name="class_quantity",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Number classes per unit",
                null=True,
                verbose_name="Class Quantity/Unit",
            ),
        ),
    ]