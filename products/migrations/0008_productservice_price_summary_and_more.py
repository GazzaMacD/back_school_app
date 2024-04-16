# Generated by Django 4.2.1 on 2023-10-24 14:18

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_alter_productserviceprice_end_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productservice",
            name="price_summary",
            field=models.CharField(
                default="not yet calculated",
                editable=False,
                help_text="Autogenerated",
                max_length=100,
                verbose_name="Product Description",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="productservice",
            name="ptype",
            field=models.CharField(
                choices=[
                    ("class", "Class"),
                    ("experience", "Learning Experience"),
                    ("book", "Book"),
                ],
                help_text="Required",
                verbose_name="Product or Service Type",
            ),
        ),
        migrations.AlterField(
            model_name="productserviceprice",
            name="end_date",
            field=models.DateTimeField(
                blank=True,
                help_text="NOT Required. Important ** Do not set this for long term prices. It is only used to have a short sale price or to terminate a long term price. It will remove the price from any public display if the current date is later than the end date",
                null=True,
                verbose_name="End date",
            ),
        ),
        migrations.AlterField(
            model_name="productserviceprice",
            name="price",
            field=models.DecimalField(
                decimal_places=0,
                help_text="Required. Pretax selling price in Japanese yen. Max digits - 10",
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                verbose_name="Price",
            ),
        ),
    ]
