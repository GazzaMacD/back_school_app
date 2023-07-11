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

    class Meta:
        icon = "desktop"
        label = "Youtube Block"


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


# =============== Multiple Choice question Blocks ======================
class MCQuestionBlock(blocks.StructBlock):
    """A block for a single question with three possible answers, one correct and two incorrect"""

    question = blocks.CharBlock(
        max_length=255,
    )
    correct_answer = blocks.CharBlock(
        max_length=50,
    )
    incorrect_answer1 = blocks.CharBlock(
        max_length=50,
    )
    incorrect_answer2 = blocks.CharBlock(
        max_length=50,
    )

    class Meta:
        icon = "help"
        label = "Multiple Choice Question"


class MCQuestionsBlock(blocks.StructBlock):
    """A block for a series of multiple choice questions with title and intro section"""

    title = blocks.CharBlock(
        max_length=30,
        help_text="A short title for the series of multiple choice questions. Max 30 chars",
    )
    intro = blocks.TextBlock(
        required=False,
        help_text="More information, if required about the test series. Not required",
    )
    questions = blocks.ListBlock(MCQuestionBlock())

    class Meta:
        icon = "help"
        label = "Multiple Choice Questions"


# =============== Conversation Blocks ======================
class TwoPersonLinesBlock(blocks.StructBlock):
    """A simple block for two peoples conversation lines"""

    person_one = blocks.CharBlock(
        max_length=255,
    )
    person_two = blocks.CharBlock(
        max_length=255,
    )

    class Meta:
        icon = "openquote"
        label = "Lines"


class ConversationBlock(blocks.StructBlock):
    """A block to compose conversations between two people for educational purposes"""

    title = blocks.CharBlock(
        max_length=30,
        help_text="A short title for the conversation. Max 30 chars",
    )
    intro = blocks.TextBlock(
        help_text="Set the scene of the conversation",
    )
    person_one_name = blocks.CharBlock(
        max_length=10,
        help_text="First person in conversation name, correlates to person one in following blocks. Please use names starting with different letters. Eg. Bob for first person and Sarah for second person. B and S in this example",
    )
    person_two_name = blocks.CharBlock(
        max_length=10,
        help_text="Secon person in conversation name, correlates to person two in following blocks.",
    )
    conversation = blocks.ListBlock(TwoPersonLinesBlock())

    class Meta:
        icon = "group"
        label = "Conversation"


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
