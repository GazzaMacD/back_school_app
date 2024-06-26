# Generated by Django 4.2.1 on 2023-09-14 08:24

from django.db import migrations, models
import django.db.models.deletion
import streams.customblocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("courses", "0008_coursedisplaydetailpage_course_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursedisplaydetailpage",
            name="course_description",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", streams.customblocks.CustomRichTextBlock()),
                    (
                        "text_width_img",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "image",
                                    streams.customblocks.CustomImageChooserBlock(
                                        help_text="Image will extend beyond text content width at large screen size. Image size: 2048px x 1280px (16/10 ratio)  ",
                                        required=True,
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.blocks.CharBlock(
                                        help_text="Optional. Caption, max length = 200",
                                        max_length=200,
                                        required=False,
                                    ),
                                ),
                                (
                                    "author",
                                    wagtail.blocks.CharBlock(
                                        help_text="Optional. The image creators name if attribution is required or nice to do, max length = 50",
                                        max_length=50,
                                        required=False,
                                    ),
                                ),
                                (
                                    "attribution_url",
                                    wagtail.blocks.URLBlock(
                                        help_text="Optional.  The url to the author or image place, max length = 100",
                                        max_length=100,
                                        required=False,
                                    ),
                                ),
                                (
                                    "license_type",
                                    wagtail.blocks.CharBlock(
                                        help_text="Optional. The type of license, eg: Creative Commons. max length = 50",
                                        max_length=50,
                                        required=False,
                                    ),
                                ),
                                (
                                    "license_url",
                                    wagtail.blocks.URLBlock(
                                        help_text="Optional. The link to relevant license. max length = 100",
                                        max_length=100,
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
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
                ],
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AddField(
            model_name="coursedisplaydetailpage",
            name="header_image",
            field=models.ForeignKey(
                help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
    ]
