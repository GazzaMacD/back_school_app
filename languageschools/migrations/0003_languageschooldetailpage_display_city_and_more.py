# Generated by Django 4.2.1 on 2024-03-05 09:16

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("languageschools", "0002_alter_languageschoollistpage_display_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="languageschooldetailpage",
            name="display_city",
            field=models.CharField(
                blank=True,
                help_text="Readonly Field, auto updated from school address. If address is changed in admin please save this again to update this field",
                verbose_name="Readonly Display City",
            ),
        ),
        migrations.AlterField(
            model_name="languageschooldetailpage",
            name="display_intro",
            field=wagtail.fields.RichTextField(
                help_text="Required. Introduction to the school",
                verbose_name="Display Introduction",
            ),
        ),
        migrations.AlterField(
            model_name="languageschooldetailpage",
            name="display_title",
            field=models.CharField(
                help_text="Required. Max length 15 characters. Japanese",
                max_length=15,
                verbose_name="Display Title",
            ),
        ),
        migrations.AlterField(
            model_name="languageschooldetailpage",
            name="ls",
            field=models.ForeignKey(
                help_text="The associated language school. Title of this page should match the name of this associated language school. If it doesn't the title and slug will be updated to match on save.",
                on_delete=django.db.models.deletion.PROTECT,
                to="languageschools.languageschool",
            ),
        ),
    ]
