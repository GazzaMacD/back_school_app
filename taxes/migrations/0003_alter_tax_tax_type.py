# Generated by Django 4.2.1 on 2023-12-30 04:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taxes", "0002_alter_tax_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tax",
            name="tax_type",
            field=models.CharField(
                choices=[("CN", "Consumption,消費税")],
                default="CN",
                help_text="Required",
                max_length=2,
                verbose_name="Tax Type",
            ),
        ),
    ]