# Generated by Django 4.2.1 on 2024-02-19 06:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0027_alter_contactpage_qas"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactpage",
            name="tel_display_number",
            field=models.CharField(
                default="Please add",
                help_text="Required. Hyphens and spaces ok for readability! Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="Telephone - Display Number",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contactpage",
            name="tel_en_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 25, 15 or less is ideal",
                max_length=25,
                verbose_name="Telephone - English Title",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contactpage",
            name="tel_jp_title",
            field=models.CharField(
                default="Please add",
                help_text="Required. Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="Telephone - Japanese Title",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contactpage",
            name="tel_number",
            field=models.CharField(
                default="Please add",
                help_text="Required. No spaces! Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="Telephone - Actual Number",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="contactpage",
            name="qa_en_title",
            field=models.CharField(
                help_text="Required. Max length 25, 15 or less is ideal",
                max_length=25,
                verbose_name="Q & A - English Title",
            ),
        ),
        migrations.AlterField(
            model_name="contactpage",
            name="qa_jp_title",
            field=models.CharField(
                help_text="Required. Max length 20 characters, 15 or less is ideal",
                max_length=20,
                verbose_name="Q & A - Japanese Title",
            ),
        ),
    ]
