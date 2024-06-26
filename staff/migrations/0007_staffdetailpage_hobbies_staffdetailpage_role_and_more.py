# Generated by Django 4.2.1 on 2023-08-16 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("staff", "0006_staffdetailpage_interview"),
    ]

    operations = [
        migrations.AddField(
            model_name="staffdetailpage",
            name="hobbies",
            field=models.CharField(
                default="reading",
                help_text="Required. Comma separated list of hobbies. Max length 255 chars",
                max_length=255,
                verbose_name="Hobbies",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="staffdetailpage",
            name="role",
            field=models.CharField(
                default="Teacher",
                help_text="Required. Max length 100 chars",
                max_length=100,
                verbose_name="Roles in company",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="staffdetailpage",
            name="profile_image",
            field=models.ForeignKey(
                help_text="Image size: 1080px x 1080px. Please optimize image size before uploading.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
    ]
