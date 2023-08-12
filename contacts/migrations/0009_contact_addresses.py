# Generated by Django 4.2.1 on 2023-08-10 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("addresses", "0003_remove_address_contact_remove_address_is_primary_and_more"),
        ("contacts", "0008_alter_contactpage_assessment_trial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="addresses",
            field=models.ManyToManyField(
                through="addresses.ContactAddress", to="addresses.address"
            ),
        ),
    ]