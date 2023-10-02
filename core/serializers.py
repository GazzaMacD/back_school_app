from rest_framework.fields import Field


class HeaderImageFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "original": value.get_rendition("original").attrs_dict,
            "medium": value.get_rendition("fill-1024x640").attrs_dict,
            "thumbnail": value.get_rendition("fill-560x350").attrs_dict,
            "alt": value.title,
        }
