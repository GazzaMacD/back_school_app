# Generated by Django 4.2.1 on 2023-09-13 09:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0004_alter_coursedisplaydetailpage_subject_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coursedisplaydetailpage",
            name="subject_slug",
            field=models.SlugField(
                blank=True,
                help_text="Read only field that get's value from the 'course' field",
                verbose_name="Subect Slug",
            ),
        ),
    ]
