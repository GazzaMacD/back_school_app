# Generated by Django 4.2.1 on 2023-11-13 15:13

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0025_learningexperiencelistpage_display_tagline_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningexperiencelistpage",
            name="intro",
            field=wagtail.fields.RichTextField(
                default="Add intro please",
                help_text="Required. For the concepts surrounding learning experiences",
                verbose_name="Introduction",
            ),
            preserve_default=False,
        ),
    ]