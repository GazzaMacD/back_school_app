# Generated by Django 4.2.1 on 2023-09-27 05:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0091_alter_page_title"),
        ("learningcenters", "0002_alter_learningcenterpage_lc"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="LearningCenterPage",
            new_name="LearningCenterDetailPage",
        ),
    ]
