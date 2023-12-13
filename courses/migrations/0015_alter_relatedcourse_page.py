# Generated by Django 4.2.1 on 2023-12-13 18:23

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0014_alter_coursedisplaylistpage_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relatedcourse",
            name="page",
            field=modelcluster.fields.ParentalKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_courses",
                to="courses.coursedisplaydetailpage",
            ),
        ),
    ]
