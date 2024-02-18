from wagtail import blocks

from wagtail.images.blocks import ImageChooserBlock

# =============== Simple Char Blocks ======================


class ShortCharBlock(blocks.StructBlock):
    """Block for lists with simple char field of 20 chars long"""

    text = blocks.CharBlock(
        required=True,
        max_length=20,
        help_text="Required. Max length 20 chars",
    )

    class Meta:
        icon = "pilcrow"
        label = "Short Text"


# =============== Image Blocks ======================


class CustomImageChooserBlock(ImageChooserBlock):
    """Customize api json response to include url string to image and thumbnail. Images are of 16/10 aspect ratio."""

    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "original": value.get_rendition("original").attrs_dict,
                "medium": value.get_rendition("fill-1024x640").attrs_dict,
                "thumbnail": value.get_rendition("fill-560x350").attrs_dict,
            }


class CustomSquareImageChooserBlock(ImageChooserBlock):
    """Customize api json response to include url string to image and thumbnail. Images are of 1/1 aspect ratio."""

    def get_api_representation(self, value, context=None):
        if value:
            return {
                "id": value.id,
                "title": value.title,
                "original": value.get_rendition("original").attrs_dict,
                "medium": value.get_rendition("fill-1024x1024").attrs_dict,
                "thumbnail": value.get_rendition("fill-560x560").attrs_dict,
            }


# =============== Rich Text Blocks ======================


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


class CustomLimitedRichTextBlock(blocks.RichTextBlock):
    """Rich text block with very limited features"""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.features = [
            "h3",
            "h4",
            "bold",
            "italic",
            "ul",
        ]

        class Meta:
            icon = "pilcrow"
            label = "Limited Rich Text"


class BoldAndLinkRichTextBlock(blocks.RichTextBlock):
    """Rich text block with bold and link only. Specificaly for example sentences"""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.max_length = 255
        self.features = [
            "bold",
            "link",
        ]

        class Meta:
            icon = "pilcrow"
            label = "Example Sentence Text"


# =============== Youtube  Blocks ======================


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


# =============== Quote  Blocks ======================


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


# =============== List Blocks ======================
class ListItemBlock(blocks.StructBlock):
    """A block for a single list item"""

    list_item = blocks.CharBlock(
        max_length=30,
        help_text="Max length 30chars.",
    )

    class Meta:
        icon = "info-circle"
        label = "List Item"


class ListBlock(blocks.StructBlock):
    """A block for a list, could be numbered or unumbered, depending on target usage"""

    liste = blocks.ListBlock(
        ListItemBlock(),
    )

    class Meta:
        icon = "list-ul"
        label = "List Block"


# =============== Simple example sentences Blocks ======================


class ExamplesListBlock(blocks.StructBlock):
    """A block for a list of simple examples"""

    sentences_list = blocks.ListBlock(BoldAndLinkRichTextBlock())

    class Meta:
        icon = "tasks"
        label = "Example Sentences or Questions List"


# =============== Wrong Right Example Blocks ======================
class WrongRightBlock(blocks.StructBlock):
    """A block for a single wrong and right sentence example"""

    wrong = blocks.CharBlock(
        max_length=255,
    )
    right = blocks.CharBlock(
        max_length=255,
    )

    class Meta:
        icon = "success"
        label = "Wrong -> Right Block"


class WrongRightListBlock(blocks.StructBlock):
    """A block for a list of wrong right examples"""

    wrong_right_list = blocks.ListBlock(WrongRightBlock())

    class Meta:
        icon = "tasks"
        label = "Wrong -> Right List"


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


# =============== Question and Answer Blocks ======================


class QuestionAnswerBlock(blocks.StructBlock):
    """A simple question and answer block"""

    question = blocks.CharBlock(
        required=True,
        max_length=255,
        help_text="Your question here. Max length 255",
    )
    answer = blocks.TextBlock(
        required=True,
        help_text="The answer to your question here.",
    )


class QuestionAnswerSeriesBlock(blocks.StructBlock):
    """A series of question and answers"""

    q_and_a_series = blocks.ListBlock(QuestionAnswerBlock())


# =============== Information Card Blocks ======================
class InfoCardBlock(blocks.StructBlock):
    """A block for card with title, image and text"""

    title = blocks.CharBlock(
        required=True,
        max_length=14,
        help_text="English title for card. Max length 14",
    )
    image = CustomImageChooserBlock(
        required=True,
        help_text="Image size: 2048px x 1280px (16/10 ratio). Please optimize image size before uploading.",
    )
    text = blocks.TextBlock(
        required=True,
        max_length=100,
        help_text="Text for card. Max length 100",
    )


class InfoCardBlockBilingual(blocks.StructBlock):
    """A block for card with title, jp title, image and text"""

    title = blocks.CharBlock(
        required=True,
        max_length=14,
        help_text="English title for card. Max length 14",
    )
    jp_title = blocks.CharBlock(
        required=True,
        max_length=10,
        help_text="Japanese Title for card. Max length 10",
    )
    image = CustomImageChooserBlock(
        required=True,
        help_text="Image size: 2048px x 1280px (16/10 ratio). Please optimize image size before uploading.",
    )
    text = blocks.TextBlock(
        required=True,
        max_length=100,
        help_text="Text for card. Max length 100",
    )

    class Meta:
        icon = "table"
        label = "Info Card Bilingual"


class InfoCardBlockOptionalPic(blocks.StructBlock):
    """A block for card with title, optional image and text"""

    title = blocks.CharBlock(
        required=True,
        max_length=20,
        help_text="Title for card. Max length 20",
    )
    image = CustomImageChooserBlock(
        required=False,
        help_text="Image size: 2048px x 1280px (16/10 ratio). Please optimize image size before uploading.",
    )
    text = blocks.TextBlock(
        required=True,
        max_length=100,
        help_text="Text for card. Max length 100",
    )

    class Meta:
        icon = "table"
        label = "Info Card Optional Pic"


class InfoCardSeriesBlock(blocks.StructBlock):
    """A block for a series of cards"""

    cards = blocks.ListBlock(InfoCardBlock())


class SquarePicCardBlock(blocks.StructBlock):
    """A block for card with square image, title, text and optional url"""

    image = CustomSquareImageChooserBlock(
        required=True,
        help_text="Image size: 2048px x 2048px (1/1 ratio). Please optimize image before uploading.",
    )
    title = blocks.CharBlock(
        required=True,
        max_length=25,
        help_text="Title for card. Max length 25",
    )
    text = blocks.TextBlock(
        required=True,
        max_length=150,
        help_text="Text for card. Max length 150",
    )
    link = blocks.CharBlock(
        required=False,
        max_length=150,
        help_text="Link url. Not required",
    )

    class Meta:
        icon = "doc-full"


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
        max_length=50,
        help_text="A short title for the conversation. Max 50 chars",
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
        help_text="Second person in conversation name, correlates to person two in following blocks.",
    )
    conversation = blocks.ListBlock(TwoPersonLinesBlock())

    class Meta:
        icon = "group"
        label = "Conversation"


# =============== Image Chooser Blocks ======================

# NOTE: image sizes still to be decided


class StandardCustomImageBlock(blocks.StructBlock):
    """Custom image block for 16/10 (2048x1280px) with caption and attribution options.
    Uses customized api representation sizes of 'original', 'medium' and 'thumbnail'"""

    image = CustomImageChooserBlock(
        required=True,
        help_text="Required. Image size: 2048px x 1280px (16/10 ratio)",
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


class SimpleImageBlock(blocks.StructBlock):
    image = CustomImageChooserBlock(
        required=True,
        help_text="Required. Image size: 2048px x 1280px (16/10 ratio)",
    )
    caption = blocks.CharBlock(
        max_length=200,
        required=False,
        help_text="Optional. Caption, max length = 200",
    )

    class Meta:
        icon = "image"
        label = "Simple Image Block"


# =============== Schedule Blocks ======================


class DateTimeDetailItemBlock(blocks.StructBlock):
    date = blocks.DateBlock(
        required=False,
        help_text="Not Required. Only needed for experience that have multiple sessions",
    )
    time = blocks.TimeBlock(
        required=True,
        help_text="Required",
    )
    detail = blocks.TextBlock(
        max_length=500,
        help_text="Required. Max length 500",
    )


class ScheduleBlock(blocks.StructBlock):
    """A block to compose a schedule"""

    title = blocks.CharBlock(
        max_length=50,
        help_text="A short title for the schedule. Max 50 chars",
    )
    intro = blocks.TextBlock(
        required=False,
        help_text="Not required. Intro to schedule below",
    )
    schedule = blocks.ListBlock(DateTimeDetailItemBlock())

    class Meta:
        icon = "time"
        label = "Schedule Block"
