# Generated by Django 4.2.1 on 2024-03-21 05:40

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0019_remove_coursedisplaylistpage_display_tagline_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursedisplaylistpage",
            name="popular_en_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 25, 15 or less is ideal",
                max_length=25,
                verbose_name="Popular - Title",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="coursedisplaylistpage",
            name="popular_jp_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="Popular - Japanese Title",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="popularenglishcourse",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.coursedisplaydetailpage",
            ),
        ),
        migrations.AlterField(
            model_name="popularenglishcourse",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="popular_courses",
                to="courses.coursedisplaylistpage",
            ),
        ),
    ]