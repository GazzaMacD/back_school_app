# Generated by Django 4.2.1 on 2023-11-15 11:22

from django.db import migrations, models
import django.db.models.deletion
import streams.customblocks
import wagtail.blocks
import wagtail.fields
import wagtail_headless_preview.models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        #("wagtailcore", "0091_alter_page_title"),
        ("products", "0028_classpriceslistpage"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClassPricesDetailPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "display_title",
                    models.CharField(
                        help_text="Required. Max length 100 characters, 45 or less is ideal",
                        max_length=100,
                        verbose_name="Display Title",
                    ),
                ),
                (
                    "display_tagline",
                    models.CharField(
                        help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the class",
                        max_length=160,
                        verbose_name="Disply Tagline",
                    ),
                ),
                (
                    "sales_point1",
                    models.CharField(
                        help_text="Required. Max length 20. Attractive sales point",
                        max_length=20,
                        verbose_name="Sales point 1",
                    ),
                ),
                (
                    "sales_point2",
                    models.CharField(
                        help_text="Required. Max length 20. Attractive sales point",
                        max_length=20,
                        verbose_name="Sales point 1",
                    ),
                ),
                (
                    "class_intro",
                    wagtail.fields.StreamField(
                        [
                            ("rich_text", streams.customblocks.CustomRichTextBlock()),
                            (
                                "beyond_text_img",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            streams.customblocks.CustomImageChooserBlock(
                                                help_text="Required. Image size: 2048px x 1280px (16/10 ratio)",
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
                                                help_text="Optional. The url to the author or image place, max length = 100",
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
                                "text_width_img",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            streams.customblocks.CustomImageChooserBlock(
                                                help_text="Required. Image size: 2048px x 1280px (16/10 ratio)",
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
                                                help_text="Optional. The url to the author or image place, max length = 100",
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
                (
                    "class_service",
                    models.OneToOneField(
                        help_text="The associated class. Title of this page should match the name of this associated class product. If it doesn't the title will be updated to match on save.",
                        limit_choices_to={"ptype": "class"},
                        on_delete=django.db.models.deletion.PROTECT,
                        to="products.productservice",
                    ),
                ),
                (
                    "header_image",
                    models.ForeignKey(
                        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail_headless_preview.models.HeadlessMixin, "wagtailcore.page"),
        ),
    ]
