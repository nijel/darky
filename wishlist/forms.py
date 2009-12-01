from django.forms import ModelForm, Form
from django.db import models
from django import forms

from wishlist.models import Gift

from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe

class NewGift(ModelForm):

    class Meta:
        model = Gift
        fields = (
            'title',
            'description',
            'url',
            'price',
            'priority',
            )
