# Generated by Django 4.2.1 on 2025-05-12 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoCall",
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
                    "host_room_url",
                    models.URLField(
                        help_text="Required. Please add the HOST url for the teacher here. Max length 1000char",
                        max_length=1000,
                    ),
                ),
                (
                    "room_url",
                    models.URLField(
                        help_text="Required. Please add the ROOM url for the teacher here. Max length 500char",
                        max_length=500,
                    ),
                ),
                ("slug", models.SlugField(editable=False, max_length=200, unique=True)),
                (
                    "teacher",
                    models.OneToOneField(
                        help_text="Required. Please choose the teacher who this video call room will be for.",
                        limit_choices_to={"is_staff": True},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="videocall",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
