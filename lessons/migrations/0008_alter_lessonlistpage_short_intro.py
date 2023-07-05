# Generated by Django 4.2.1 on 2023-07-05 08:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0007_remove_lessonlistpage_jp_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lessonlistpage",
            name="short_intro",
            field=models.CharField(
                help_text="An introduction to the free lessons concept. max length 90 chars",
                max_length=160,
                verbose_name="Short Intro",
            ),
        ),
    ]