# Generated by Django 4.2.1 on 2023-08-14 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0019_contact_child_of"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="child_of",
            field=models.ManyToManyField(
                blank=True,
                help_text="Not required",
                limit_choices_to={"ind_or_org": 0},
                related_name="guardian_of",
                to="contacts.contact",
            ),
        ),
    ]