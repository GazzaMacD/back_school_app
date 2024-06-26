# Generated by Django 4.2.1 on 2023-08-04 08:28

from django.db import migrations
import streams.customblocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0007_contactpage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactpage",
            name="assessment_trial",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", streams.customblocks.CustomRichTextBlock()),
                    (
                        "youtube",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "src",
                                    wagtail.blocks.URLBlock(
                                        help_text="Get src from in the youtube embed code, include start if needed.",
                                        max_length=255,
                                        required=True,
                                    ),
                                ),
                                (
                                    "short",
                                    wagtail.blocks.BooleanBlock(
                                        help_text="Tick this box if the video is a short, i.e vertical format",
                                        required=False,
                                    ),
                                ),
                                (
                                    "limit",
                                    wagtail.blocks.BooleanBlock(
                                        help_text="Tick this box if you would like to limit recommended videos to this channel",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "info_cards",
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
