# Generated by Django 4.2.1 on 2024-01-20 06:28

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0036_alter_productservice_class_type_and_more"),
        ("home", "0006_homepage_testimonial_en_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="price_en_title",
            field=models.CharField(
                default="FILL IN PLEASE",
                help_text="Required. Max length 25, 15 or less is ideal",
                max_length=25,
                verbose_name="Class Prices - English Title",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="homepage",
            name="price_jp_title",
            field=models.CharField(
                default="FILL IN PLEASE",
                help_text="Required. Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="Class Prices - Japanese Title",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="HomePrices",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "class_price",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.classpricesdetailpage",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="home_class_prices",
                        to="home.homepage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]