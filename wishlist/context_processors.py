from django.contrib.auth.models import User


def wishlist_context(request):
    return {"all_users": User.objects.filter(is_active=True)}
