# Generated by Django 4.2.1 on 2023-11-08 09:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0019_learningexperiencedetailpage_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningexperiencedetailpage",
            name="end_date",
            field=models.DateField(
                blank=True,
                default=django.utils.timezone.now,
                help_text="Read only field that gets value from 'learning_experience'",
                verbose_name="Start Date",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="learningexperiencedetailpage",
            name="start_date",
            field=models.DateField(
                blank=True,
                default=django.utils.timezone.now,
                help_text="Read only field that gets value from 'learning_experience'",
                verbose_name="Start Date",
            ),
            preserve_default=False,
        ),
    ]
