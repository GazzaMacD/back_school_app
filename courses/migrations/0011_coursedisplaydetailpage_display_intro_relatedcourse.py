# Generated by Django 4.2.1 on 2023-09-14 10:07

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0010_coursedisplaydetailpage_course_content_points"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursedisplaydetailpage",
            name="display_intro",
            field=models.TextField(
                default="Default intro - please change",
                help_text="Required. Max length 150.",
                max_length=150,
                verbose_name="Display Introduction",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="RelatedCourse",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.coursedisplaydetailpage",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_courses",
                        to="courses.coursedisplaydetailpage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]