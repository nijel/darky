from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^darky/', include('darky.foo.urls')),
    (r'^$', 'wishlist.views.overview'),
    (r'^gift/(?P<userid>[^/]*)/(?P<giftid>\d*)/$', 'wishlist.views.gift'),
    (r'^create/$', 'wishlist.views.create'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Static media for development
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': './media'}),
)
