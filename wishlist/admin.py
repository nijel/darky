from wishlist.models import Gift
from django.contrib import admin

class GiftAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'buyer', 'url', 'price', 'priority')
    list_filter = ('owner', 'buyer')

admin.site.register(Gift, GiftAdmin)
