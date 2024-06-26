# Generated by Django 4.2.1 on 2023-11-13 06:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0022_productservice_tax_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="productserviceprice",
            name="display_name",
            field=models.CharField(
                default="Please change this",
                help_text="Required. Max length 200 characters. Will in many cases be Japanese name.",
                max_length=200,
                verbose_name="Display Name",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="productserviceprice",
            name="name",
            field=models.CharField(
                help_text="Required. Max length 200 characters. In English please.",
                max_length=200,
                verbose_name="Name",
            ),
        ),
    ]
