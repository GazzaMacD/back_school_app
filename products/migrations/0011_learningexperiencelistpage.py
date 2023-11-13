# Generated by Django 4.2.1 on 2023-10-26 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0091_alter_page_title"),
        ("products", "0010_learningexperience_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningExperienceListPage",
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
                        help_text="Required. Max length 100 characters, 45 or less is ideal",
                        max_length=100,
                        verbose_name="Display Title",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]