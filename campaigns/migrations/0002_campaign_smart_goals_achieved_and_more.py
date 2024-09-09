# Generated by Django 4.2.1 on 2024-08-08 09:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("campaigns", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="smart_goals_achieved",
            field=models.BooleanField(
                default=False,
                help_text="Required. Completed after campaign results finalized. Please consider 'S' in SMART to answer this question",
                verbose_name="Smart Goals Achieved",
            ),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="description",
            field=models.TextField(
                default="\n[BRIEF]\n\n\n\n\n[SMART]\n\nS: \n\nM: \n\nA: \n\nR: \n\nT: \n\n",
                help_text="Description of key elements of campaign. Please use SMART here.",
                verbose_name="Campaign Description",
            ),
        ),
    ]