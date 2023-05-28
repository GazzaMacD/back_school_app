# Generated by Django 4.2.1 on 2023-05-27 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="LessonListPage",
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
                    "jp_title",
                    models.CharField(
                        help_text="Required. Max length 70 characters, 60 or less is ideal",
                        max_length=70,
                        verbose_name="Japanese Title",
                    ),
                ),
            ],
            options={
                "verbose_name": "Lesson list page",
            },
            bases=("wagtailcore.page",),
        ),
    ]
