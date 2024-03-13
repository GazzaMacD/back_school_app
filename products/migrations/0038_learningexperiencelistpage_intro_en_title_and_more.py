# Generated by Django 4.2.1 on 2024-03-06 05:03

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0037_remove_learningexperiencelistpage_display_tagline_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningexperiencelistpage",
            name="intro_en_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 35",
                max_length=35,
                verbose_name="Intro - English Title",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="learningexperiencelistpage",
            name="intro_jp_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="Intro - Japanese Title",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="learningexperiencelistpage",
            name="intro",
            field=wagtail.fields.RichTextField(
                help_text="Required. Explain the concepts surrounding learning experiences",
                verbose_name="Intro - detail",
            ),
        ),
    ]