from django.conf.urls import include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import django.contrib.auth.views
import django.views.static

import wishlist.views

admin.autodiscover()

urlpatterns = [
    # Example:
    # (r'^darky/', include('darky.foo.urls')),
    url(r'^$', wishlist.views.overview),
    url(r'^create/$', wishlist.views.create),
    url(r'^buy/$', wishlist.views.buylist),

    url(r'^login/$', django.contrib.auth.views.login),
    url(r'^logout/$', django.contrib.auth.views.logout),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Static media for development
    url(
        r'^media/(?P<path>.*)$',
        django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}
    ),

    # Need to be last to avoid conflicts on userid
    url(r'^(?P<userid>[^/]*)/$', wishlist.views.userlist),
    url(
        r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/$',
        wishlist.views.gift,
        name='gift'
    ),
    url(
        r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/buy/$',
        wishlist.views.buy,
        name='buy'
    ),
    url(
        r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/revoke/$',
        wishlist.views.revoke,
        name='revoke'
    ),
    url(
        r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/edit/$',
        wishlist.views.edit,
        name='edit'
        ),
    url(
        r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/delete/$',
        wishlist.views.delete,
        name='delete'
    ),
]
