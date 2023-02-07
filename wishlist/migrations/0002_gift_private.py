from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wishlist", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gift",
            name="private",
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
