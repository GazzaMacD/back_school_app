# Generated by Django 4.2.1 on 2023-10-10 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("languageschools", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SuperSassSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="AUTOGENERATED. Please DO NOT modify this value",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "schedule_url",
                    models.URLField(
                        help_text="Required. Please add the url for the teacher here .Please check name and ls are correct.",
                        max_length=300,
                    ),
                ),
                (
                    "language_school",
                    models.ForeignKey(
                        help_text="Required. Please choose the language school this schedule is for.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="language_schools",
                        to="languageschools.languageschool",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        help_text="Required. Please choose the teacher who this schedule is for.",
                        limit_choices_to={"is_staff": True},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="super_sass_schedules",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
