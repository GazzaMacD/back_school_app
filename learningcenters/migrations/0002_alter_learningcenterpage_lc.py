# Generated by Django 4.2.1 on 2023-09-27 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("learningcenters", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="learningcenterpage",
            name="lc",
            field=models.ForeignKey(
                help_text="The associated learning center. Title of this page should match the name of this associated learning center. If it doesn't the title will be updated to match on save.",
                on_delete=django.db.models.deletion.PROTECT,
                to="learningcenters.learningcenter",
            ),
        ),
    ]
