# Generated by Django 4.2.1 on 2023-09-29 12:45

from django.db import migrations, models
import django.db.models.deletion
import streams.customblocks
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("addresses", "0007_address_is_learning_center"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        #("wagtailcore", "0091_alter_page_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="LanguageSchool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Name of the language school in English. Will be used as the name for the public page title.",
                        max_length=100,
                        verbose_name="name",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Slug must be all lower case and separated by hyphens if necessary. This slug value will be used in the public urls",
                        max_length=100,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        help_text="This address will be used in public facing displays. Please make sure to mark 'is_language_school' as true if entering a new address",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="addresses.address",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LanguageSchoolListPage",
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
                    "display_intro",
                    wagtail.fields.RichTextField(
                        help_text="Required.", verbose_name="Display Introduction"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="LanguageSchoolDetailPage",
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
                    "display_intro",
                    wagtail.fields.RichTextField(
                        help_text="Required.", verbose_name="Display Introduction"
                    ),
                ),
                (
                    "display_map",
                    models.TextField(
                        help_text='Required. Please paste the iframe imbed code here. Please remove both the height="....." and width="....." attributes from the code before saving otherwise the map will not display as intended on the site',
                        verbose_name="Display map",
                    ),
                ),
                (
                    "access_info",
                    models.TextField(
                        help_text="Please explain all modes of access relevent to this language school",
                        verbose_name="Access Information",
                    ),
                ),
                (
                    "ls_photos",
                    wagtail.fields.StreamField(
                        [
                            (
                                "simple_image_block",
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
                                    ]
                                ),
                            )
                        ],
                        null=True,
                        use_json_field=True,
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
                (
                    "ls",
                    models.ForeignKey(
                        help_text="The associated language school. Title of this page should match the name of this associated language school. If it doesn't the title will be updated to match on save.",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="languageschools.languageschool",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
