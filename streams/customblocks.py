from wagtail import blocks

from wagtail.images.blocks import ImageChooserBlock


class CustomImageChooserBlock(ImageChooserBlock):
    """Customize api json response to include url string to image and thumbnail"""

    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "original": value.get_rendition("original").attrs_dict,
                "thumbnail": value.get_rendition("fill-240x240").attrs_dict,
            }


class CustomRichTextBlock(blocks.RichTextBlock):
    """Rich text block with limited features"""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.features = [
            "h2",
            "h3",
            "h4",
            "link",
            "bold",
            "italic",
            "ol",
            "ul",
        ]

        class Meta:
            icon = "pilcrow"
            label = "Rich Text"


class YoutubeBlock(blocks.StructBlock):
    """Block to add responsive imbeded youtube video"""

    src = blocks.URLBlock(
        required=True,
        max_length=255,
        help_text="Get src from in the youtube embed code, include start if needed.",
    )
    short = blocks.BooleanBlock(
        required=False,
        help_text="Tick this box if the video is a short, i.e vertical format",
    )
    limit = blocks.BooleanBlock(
        required=False,
        help_text="Tick this box if you would like to limit recommended videos to this channel",
    )


class BlockQuoteBlock(blocks.StructBlock):
    """Block for correctly structured block quotes"""

    author = blocks.CharBlock(
        required=True,
        max_length=40,
        help_text="The quote author's full name",
    )
    quote = blocks.TextBlock(required=True, help_text="The quote itself")
    citation_url = blocks.URLBlock(
        required=False,
        help_text="Link url from where quotation comes from, if available",
    )
    citation_source = blocks.CharBlock(
        required=True,
        max_length=40,
        help_text=" The title of the creative work from which the quote comes",
    )

    class Meta:
        icon = "openquote"
        label = "Block quotation"


# =============== Image Chooser Blocks ======================

# NOTE: image sizes still to be decided


class FullWidthImage(blocks.StructBlock):
    """A full width image at large screen size with  optional caption and attribution"""

    image = CustomImageChooserBlock(
        required=True,
        help_text="Full width at large screen size. Use an image NOTE: TO BE DECIDED***",
    )
    caption = blocks.CharBlock(
        max_length=200,
        required=False,
        help_text="Optional. Caption, max length = 200",
    )
    author = blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Optional. The image creators name if attribution is required or nice to do, max length = 50",
    )
    attribution_url = blocks.URLBlock(
        max_length=100,
        required=False,
        help_text="Optional. The url to the author or image place, max length = 100",
    )
    license_type = blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Optional. The type of license, eg: Creative Commons. max length = 50",
    )
    license_url = blocks.URLBlock(
        max_length=100,
        required=False,
        help_text="Optional. The link to relevant license. max length = 100",
    )

    class Meta:
        icon = "image"
        label = "Full Width Image"


class BeyondContentWidthImage(blocks.StructBlock):
    """An image that will project beyond the text content column on both sides
    at medium and large screen size with an optional caption and attribution"""

    image = CustomImageChooserBlock(
        required=True,
        help_text="Image will extend beyond text content width at large screen size. Use an image **TO BE DECIDED***",
    )
    caption = blocks.CharBlock(
        max_length=200,
        required=False,
        help_text="Optional. Caption, max length = 200",
    )
    author = blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Optional. The image creators name if attribution is required or nice to do, max length = 50",
    )
    attribution_url = blocks.URLBlock(
        max_length=100,
        required=False,
        help_text="Optional. The url to the author or image place, max length = 100",
    )
    license_type = blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Optional. The type of license, eg: Creative Commons. max length = 50",
    )
    license_url = blocks.URLBlock(
        max_length=100,
        required=False,
        help_text="Optional. The link to relevant license. max length = 100",
    )

    class Meta:
        icon = "image"
        label = "Beyond Content Image"


class ContentWidthImage(blocks.StructBlock):
    """An image that will line up with the text content with optional caption and attribution"""

    image = CustomImageChooserBlock(
        required=True,
        help_text="Image will extend beyond text content width at large screen size. Use an image **TO BE DECIDED***",
    )
    caption = blocks.CharBlock(
        max_length=200,
        required=False,
        help_text="Optional. Caption, max length = 200",
    )
    author = blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Optional. The image creators name if attribution is required or nice to do, max length = 50",
    )
    attribution_url = blocks.URLBlock(
        max_length=100,
        required=False,
        help_text="Optional.  The url to the author or image place, max length = 100",
    )
    license_type = blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Optional. The type of license, eg: Creative Commons. max length = 50",
    )
    license_url = blocks.URLBlock(
        max_length=100,
        required=False,
        help_text="Optional. The link to relevant license. max length = 100",
    )

    class Meta:
        icon = "image"
        label = " Content Width Image"
