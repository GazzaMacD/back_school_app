# Generated by Django 4.2.1 on 2024-03-29 08:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0030_alter_lessondetailpage_display_tagline"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lessonlistpage",
            name="display_tagline",
        ),
    ]
