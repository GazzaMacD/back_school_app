# Generated by Django 4.2.1 on 2023-11-07 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("addresses", "0010_alter_experienceaddress_options"),
        ("products", "0018_learningexperiencedetailpage_display_map"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningexperiencedetailpage",
            name="address",
            field=models.ForeignKey(
                blank=True,
                help_text="Not required but preferable if applicable",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="addresses.experienceaddress",
            ),
        ),
    ]