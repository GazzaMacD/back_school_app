# Generated by Django 4.2.1 on 2023-10-25 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_productservice_price_summary_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productserviceprice",
            name="is_limited_sale",
            field=models.BooleanField(
                default=False,
                help_text="If ticked, please make sure to add the end date",
                verbose_name="Is Limited Sale Price",
            ),
        ),
        migrations.AlterField(
            model_name="productservice",
            name="price_summary",
            field=models.CharField(
                editable=False,
                help_text="Autogenerated",
                max_length=100,
                verbose_name="Price Summary",
            ),
        ),
        migrations.AlterField(
            model_name="productservice",
            name="ptype",
            field=models.CharField(
                choices=[
                    ("class", "Class"),
                    ("experience", "Learning Experience"),
                    ("book", "Book"),
                    ("joiningfee", "Joining Fee"),
                ],
                help_text="Required",
                verbose_name="Product or Service Type",
            ),
        ),
    ]