# Generated by Django 4.2.1 on 2024-02-16 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("about", "0006_remove_aboutpage_history_tagline_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutpage",
            name="display_title",
            field=models.CharField(
                help_text="Required. Max length 15 characters. Japanese",
                max_length=15,
                verbose_name="Display Title",
            ),
        ),
    ]
