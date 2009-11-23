from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy

import markdown

class Present(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(
        max_length = 250
        )
    description = models.TextField(
        help_text = ugettext_lazy('Description, you can use markdown.')
        )
    description_html = models.TextField(
        editable = False,
        blank = True
        )
    url = models.URLField()

    def save(self):
        self.description_html = markdown.markdown(self.description)
        super(Category, self).save()
