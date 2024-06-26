# Generated by Django 4.2.1 on 2024-02-16 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0022_alter_contactpage_assessment_trial_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contactpage",
            name="ja_title",
        ),
        migrations.RemoveField(
            model_name="contactpage",
            name="short_intro",
        ),
        migrations.AddField(
            model_name="contactpage",
            name="display_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 15 characters. Japanese",
                max_length=15,
                verbose_name="Display Title",
            ),
            preserve_default=False,
        ),
    ]
