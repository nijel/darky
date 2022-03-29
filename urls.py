import django.contrib.auth.views
import django.views.static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

import wishlist.views

admin.autodiscover()

urlpatterns = [
    re_path(r"^$", wishlist.views.overview),
    re_path(r"^create/$", wishlist.views.create),
    re_path(r"^buy/$", wishlist.views.buylist),
    path("login/", auth_views.LoginView.as_view()),
    path("logout/", auth_views.LogoutView.as_view()),
    path("admin/", admin.site.urls),
    # Static media for development
    re_path(
        r"^media/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
    # Need to be last to avoid conflicts on userid
    re_path(r"^(?P<userid>[^/]*)/$", wishlist.views.userlist),
    re_path(r"^(?P<userid>[^/]*)/(?P<giftid>\d*)/$", wishlist.views.gift, name="gift"),
    re_path(
        r"^(?P<userid>[^/]*)/(?P<giftid>\d*)/buy/$", wishlist.views.buy, name="buy"
    ),
    re_path(
        r"^(?P<userid>[^/]*)/(?P<giftid>\d*)/revoke/$",
        wishlist.views.revoke,
        name="revoke",
    ),
    re_path(
        r"^(?P<userid>[^/]*)/(?P<giftid>\d*)/edit/$", wishlist.views.edit, name="edit"
    ),
    re_path(
        r"^(?P<userid>[^/]*)/(?P<giftid>\d*)/delete/$",
        wishlist.views.delete,
        name="delete",
    ),
]
