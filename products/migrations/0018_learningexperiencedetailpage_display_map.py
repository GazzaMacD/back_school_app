# Generated by Django 4.2.1 on 2023-11-07 07:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0017_experiencerelatedlessons"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningexperiencedetailpage",
            name="display_map",
            field=models.TextField(
                default="",
                help_text='Required. Please paste the iframe imbed code here. Please remove both the height="....." and width="....." attributes from the code before saving otherwise the map will not display as intended on the site',
                verbose_name="Display map",
            ),
            preserve_default=False,
        ),
    ]
