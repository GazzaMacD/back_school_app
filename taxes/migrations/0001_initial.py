# Generated by Django 4.2.1 on 2023-11-10 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tax",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Required. Max length 100. Must be a unique identifying name in English for this tax",
                        max_length=100,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "tax_type",
                    models.CharField(
                        choices=[("CN", "Consumption,消費税")],
                        default="CN",
                        help_text="Required",
                        verbose_name="Tax Type",
                    ),
                ),
                (
                    "rate",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Required. Max digits 5. Max decimal places 2.",
                        max_digits=10,
                        verbose_name="Tax rate",
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(
                        help_text="Required. Please make sure to set when this rate became officially applicable. It is generally never changed",
                        verbose_name="Start date",
                    ),
                ),
                (
                    "end_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="Not Required. **IMPORTANT. Do not set this until the tax is officially declared null and void. Make sure to change all products or other tables that use this rate before setting this. Thankyou.",
                        null=True,
                        verbose_name="End date",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
