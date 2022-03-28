from django.contrib import admin

from wishlist.models import Gift


class GiftAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "buyer", "private", "url", "price", "priority")
    list_filter = ("owner", "buyer", "private")


admin.site.register(Gift, GiftAdmin)
