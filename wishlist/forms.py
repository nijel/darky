from django.forms import ModelForm

from wishlist.models import Gift


class NewGift(ModelForm):
    class Meta:
        model = Gift
        fields = (
            "title",
            "description",
            "url",
            "price",
            "priority",
        )
