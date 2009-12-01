from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^darky/', include('darky.foo.urls')),
    (r'^$', 'wishlist.views.overview'),
    (r'^create/$', 'wishlist.views.create'),
    (r'^buy/$', 'wishlist.views.buylist'),

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Static media for development
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': './media'}),

    # Need to be last to avoid conflicts on userid
    (r'^(?P<userid>[^/]*)/$', 'wishlist.views.userlist'),
    (r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/$', 'wishlist.views.gift'),
    (r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/buy/$', 'wishlist.views.buy'),
    (r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/revoke/$', 'wishlist.views.revoke'),
    (r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/edit/$', 'wishlist.views.edit'),
    (r'^(?P<userid>[^/]*)/(?P<giftid>\d*)/delete/$', 'wishlist.views.delete'),
)
