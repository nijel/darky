from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy

import markdown

class Gift(models.Model):
    owner = models.ForeignKey(User, related_name = 'present_set')
    buyer = models.ForeignKey(User, null = True, blank = True, related_name = 'given_set')
    title = models.CharField(
        max_length = 250
        )
    description = models.TextField(
        help_text = ugettext_lazy('Description, you can use markdown.'),
        blank = True
        )
    description_html = models.TextField(
        editable = False,
        blank = True
        )
    url = models.URLField(blank = True)
    price = models.IntegerField(null = True, blank = True)

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.owner.get_full_name())

    def save(self):
        self.description_html = markdown.markdown(self.description)
        super(Gift, self).save()
