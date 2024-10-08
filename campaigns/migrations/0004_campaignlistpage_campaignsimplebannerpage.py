# Generated by Django 4.2.1 on 2024-08-12 05:13

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields
import wagtail_headless_preview.models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0091_remove_revision_submitted_for_moderation"),
        ("campaigns", "0003_alter_campaign_description_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CampaignListPage",
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
                        help_text="Required. Max length 20 characters. Japanese",
                        max_length=20,
                        verbose_name="Display Title",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail_headless_preview.models.HeadlessMixin, "wagtailcore.page"),
        ),
        migrations.CreateModel(
            name="CampaignSimpleBannerPage",
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
                    "campaign_page_type",
                    models.CharField(
                        default="simple_banner",
                        editable=False,
                        help_text="Auto generated",
                        max_length=20,
                        verbose_name="Campaign Page Type",
                    ),
                ),
                (
                    "color_type",
                    models.CharField(
                        choices=[("lightblue", "Light Blue")],
                        help_text="Required. Will determine the color scheme of the banner and page",
                        max_length=10,
                        verbose_name="Banner Color",
                    ),
                ),
                (
                    "name_ja",
                    models.CharField(
                        help_text="Required. Max length 18 chars. Will be name of campaign on banner. Please avoid using 'キャンペーン' in the name. It is already on the banner below this name.",
                        max_length=18,
                        verbose_name="Japanese Campaign Name",
                    ),
                ),
                (
                    "offer",
                    models.CharField(
                        help_text="Required. Max length 20 chars. The offer, biggest text on the banner",
                        max_length=20,
                        verbose_name="Campaign Offer",
                    ),
                ),
                (
                    "tagline",
                    models.CharField(
                        help_text="Required. Max length 100 chars. Succint additional text to add marketing value to the banner",
                        max_length=100,
                        verbose_name="Tagline",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        blank=True,
                        help_text="Read only field that gets value from 'campaign'",
                        verbose_name="Start Date",
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        blank=True,
                        help_text="Read only field that gets value from 'campaign'",
                        verbose_name="End Date",
                    ),
                ),
                (
                    "additional_details",
                    wagtail.fields.RichTextField(
                        help_text="Required. Please add any additional info here. Conditions links etc",
                        verbose_name="Additional details",
                    ),
                ),
                (
                    "campaign",
                    models.OneToOneField(
                        help_text="The associated campaign. IMPORTANT. PLease make sure the title on this page is the same as the campaign name.",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="campaigns.campaign",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail_headless_preview.models.HeadlessMixin, "wagtailcore.page"),
        ),
    ]
