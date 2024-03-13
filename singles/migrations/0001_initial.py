# Generated by Django 4.2.1 on 2024-03-01 11:26

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields
import wagtail_headless_preview.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
    ]

    operations = [
        migrations.CreateModel(
            name="PrivacyPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "display_title",
                    models.CharField(
                        help_text="Required. Max length 15 characters. Japanese",
                        max_length=15,
                        verbose_name="Display Title",
                    ),
                ),
                ("content", wagtail.fields.RichTextField()),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail_headless_preview.models.HeadlessMixin, "wagtailcore.page"),
        ),
    ]