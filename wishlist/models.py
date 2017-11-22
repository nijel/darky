from django.db import models

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy

import markdown

PRIORITY_CHOICES = (
    (1, ugettext_lazy('Very low')),
    (2, ugettext_lazy('Low')),
    (3, ugettext_lazy('Standard')),
    (4, ugettext_lazy('High')),
    (5, ugettext_lazy('Very high')),
)


class Gift(models.Model):
    owner = models.ForeignKey(
        User, related_name='present_set'
    )
    buyer = models.ForeignKey(
        User, null=True, blank=True, related_name='given_set'
    )
    private = models.BooleanField(
        default=False
    )
    title = models.CharField(
        ugettext_lazy('Title'), max_length=250
    )
    description = models.TextField(
        ugettext_lazy('Description'),
        help_text=ugettext_lazy(
            'You can use <a href="http://daringfireball.net'
            '/projects/markdown/syntax">Markdown</a>.'
        ),
        blank=True
    )
    description_html = models.TextField(
        editable=False,
        blank=True
    )
    url = models.URLField(
        ugettext_lazy('Link'), null=True, blank=True
    )
    price = models.IntegerField(
        ugettext_lazy('Expected price'), null=True, blank=True
    )
    priority = models.IntegerField(
        ugettext_lazy('Priority'), choices=PRIORITY_CHOICES, default=3
    )

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.owner.get_full_name())

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super(Gift, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self, part='gift'):
        return (
            part,
            (),
            {'giftid': self.id, 'userid': self.owner.username}
        )

    def get_delete_url(self):
        return self.get_absolute_url('delete')

    def get_edit_url(self):
        return self.get_absolute_url('edit')

    def get_buy_url(self):
        return self.get_absolute_url('buy')

    def get_revoke_url(self):
        return self.get_absolute_url('revoke')

    def buy(self, user):
        self.buyer = user
        self.save()

    def revoke(self):
        self.buyer = None
        self.save()
