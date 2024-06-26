# Generated by Django 4.2.1 on 2023-10-18 13:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.blocks
import wagtail.fields
import wagtail_headless_preview.models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        #("wagtailcore", "0091_alter_page_title"),
        ("testimonials", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestimonialDetailPage",
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
                    "customer_name",
                    models.CharField(
                        help_text="Required. Max length 100 chars",
                        max_length=100,
                        verbose_name="Customer name",
                    ),
                ),
                (
                    "occupation",
                    models.CharField(
                        help_text="Required. Max length 100 chars",
                        max_length=100,
                        verbose_name="Occupation of customer",
                    ),
                ),
                (
                    "organization_name",
                    models.CharField(
                        blank=True,
                        help_text="Not required but adds to veracity of testimonial. Max length 100 chars.",
                        max_length=100,
                        verbose_name="Organization affiliated with",
                    ),
                ),
                (
                    "organization_url",
                    models.URLField(
                        blank=True,
                        help_text="Not required but adds to veracity of testimonial. Max length 100 chars.",
                        max_length=100,
                        verbose_name="Url for organization",
                    ),
                ),
                (
                    "published_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="IMPORTANT NOTE: This date will affect the order on list pages.",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Required. Max length 300 chars. A short comment about the school to display in places on site.",
                        max_length=100,
                        verbose_name="Short Comment",
                    ),
                ),
                (
                    "customer_interview",
                    wagtail.fields.StreamField(
                        [
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
                                "conversation",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.CharBlock(
                                                help_text="A short title for the conversation. Max 30 chars",
                                                max_length=30,
                                            ),
                                        ),
                                        (
                                            "intro",
                                            wagtail.blocks.TextBlock(
                                                help_text="Set the scene of the conversation"
                                            ),
                                        ),
                                        (
                                            "person_one_name",
                                            wagtail.blocks.CharBlock(
                                                help_text="First person in conversation name, correlates to person one in following blocks. Please use names starting with different letters. Eg. Bob for first person and Sarah for second person. B and S in this example",
                                                max_length=10,
                                            ),
                                        ),
                                        (
                                            "person_two_name",
                                            wagtail.blocks.CharBlock(
                                                help_text="Secon person in conversation name, correlates to person two in following blocks.",
                                                max_length=10,
                                            ),
                                        ),
                                        (
                                            "conversation",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "person_one",
                                                            wagtail.blocks.CharBlock(
                                                                max_length=255
                                                            ),
                                                        ),
                                                        (
                                                            "person_two",
                                                            wagtail.blocks.CharBlock(
                                                                max_length=255
                                                            ),
                                                        ),
                                                    ]
                                                )
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
                    "customer_image",
                    models.ForeignKey(
                        help_text="Image size: 1080px x 1080px. Please optimize image size before uploading.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Testimonial Detail Page",
                "verbose_name_plural": "Testimonial Detail Pages",
                "ordering": ["-published_date"],
            },
            bases=(wagtail_headless_preview.models.HeadlessMixin, "wagtailcore.page"),
        ),
    ]
