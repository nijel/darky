from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Gift",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=250, verbose_name="Title")),
                (
                    "description",
                    models.TextField(
                        help_text='You can use <a href="http://daringfireball.net/projects/markdown/syntax">markdown</a>.',
                        verbose_name="Description",
                        blank=True,
                    ),
                ),
                ("description_html", models.TextField(editable=False, blank=True)),
                (
                    "url",
                    models.URLField(
                        null=True,
                        verbose_name="Link",
                        blank=True,
                    ),
                ),
                (
                    "price",
                    models.IntegerField(
                        null=True,
                        verbose_name="Expected price",
                        blank=True,
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        default=3,
                        verbose_name="Priority",
                        choices=[
                            (1, "Very low"),
                            (2, "Low"),
                            (3, "Standard"),
                            (4, "High"),
                            (5, "Very high"),
                        ],
                    ),
                ),
                (
                    "buyer",
                    models.ForeignKey(
                        related_name="given_set",
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        related_name="present_set",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.deletion.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
