# Generated by Django 4.2.1 on 2023-12-15 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0015_alter_relatedcourse_page"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coursedisplaydetailpage",
            name="display_intro",
        ),
        migrations.AddField(
            model_name="coursedisplaydetailpage",
            name="display_tagline",
            field=models.CharField(
                default="PLEASE ADD",
                help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the course",
                max_length=160,
                verbose_name="Disply Tagline",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="coursedisplaydetailpage",
            name="course",
            field=models.OneToOneField(
                help_text="The associated course, the page title should match exactly the name of this course",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="course_detail_page",
                to="courses.course",
            ),
        ),
    ]
