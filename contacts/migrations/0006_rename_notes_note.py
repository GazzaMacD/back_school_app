# Generated by Django 4.2.1 on 2023-07-29 08:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0005_notes"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Notes",
            new_name="Note",
        ),
    ]
