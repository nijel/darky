import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy

PRIORITY_CHOICES = (
    (1, gettext_lazy("Very low")),
    (2, gettext_lazy("Low")),
    (3, gettext_lazy("Standard")),
    (4, gettext_lazy("High")),
    (5, gettext_lazy("Very high")),
)


class Gift(models.Model):
    owner = models.ForeignKey(
        User, related_name="present_set", on_delete=models.deletion.CASCADE
    )
    buyer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="given_set",
        on_delete=models.deletion.SET_NULL,
    )
    private = models.BooleanField(default=False)
    title = models.CharField(gettext_lazy("Title"), max_length=250)
    description = models.TextField(
        gettext_lazy("Description"),
        help_text=gettext_lazy(
            'You can use <a href="http://daringfireball.net'
            '/projects/markdown/syntax">Markdown</a>.'
        ),
        blank=True,
    )
    description_html = models.TextField(editable=False, blank=True)
    url = models.URLField(gettext_lazy("Link"), null=True, blank=True, max_length=500)
    price = models.IntegerField(gettext_lazy("Expected price"), null=True, blank=True)
    priority = models.IntegerField(
        gettext_lazy("Priority"), choices=PRIORITY_CHOICES, default=3
    )

    def __unicode__(self):
        return f"{self.title} ({self.owner.get_full_name()})"

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self, part="gift"):
        return reverse(
            "gift", kwargs={"giftid": self.id, "userid": self.owner.username}
        )

    def get_delete_url(self):
        return self.get_absolute_url("delete")

    def get_edit_url(self):
        return self.get_absolute_url("edit")

    def get_buy_url(self):
        return self.get_absolute_url("buy")

    def get_revoke_url(self):
        return self.get_absolute_url("revoke")

    def buy(self, user):
        self.buyer = user
        self.save()

    def revoke(self):
        self.buyer = None
        self.save()
