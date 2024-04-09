# Generated by Django 4.2.1 on 2024-03-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0020_coursedisplaylistpage_popular_en_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursedisplaylistpage",
            name="english_en_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 25, 15 or less is ideal",
                max_length=25,
                verbose_name="English - Title",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="coursedisplaylistpage",
            name="english_jp_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="English - Japanese Title",
            ),
            preserve_default=False,
        ),
    ]