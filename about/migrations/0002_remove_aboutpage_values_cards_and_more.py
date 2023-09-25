# Generated by Django 4.2.1 on 2023-09-23 04:58

from django.db import migrations
import streams.customblocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("about", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aboutpage",
            name="values_cards",
        ),
        migrations.AddField(
            model_name="aboutpage",
            name="values_content",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", streams.customblocks.CustomRichTextBlock()),
                    (
                        "value_cards",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "cards",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "title",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Title for card. Max length 20",
                                                        max_length=20,
                                                        required=True,
                                                    ),
                                                ),
                                                (
                                                    "image",
                                                    streams.customblocks.CustomImageChooserBlock(
                                                        help_text="Image size: 2048px x 1280px (16/10 ratio). Please optimize image size before uploading.",
                                                        required=True,
                                                    ),
                                                ),
                                                (
                                                    "text",
                                                    wagtail.blocks.TextBlock(
                                                        help_text="Text for card. Max length 100",
                                                        max_length=100,
                                                        required=True,
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    ),
                ],
                null=True,
                use_json_field=True,
            ),
        ),
    ]
