from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User

from wishlist.models import Gift
from wishlist.forms import NewGift


@login_required
def overview(request):
    gifts = Gift.objects.all().order_by('owner', '-priority')
    return render(request, 'overview.html', {'gifts': gifts})


@login_required
def userlist(request, userid):
    user = get_object_or_404(User, username=userid)
    gifts = Gift.objects.filter(owner=user).order_by('-priority')
    return render(request, 'userlist.html', {'gifts': gifts, 'listuser': user})


@login_required
def buylist(request):
    gifts = Gift.objects.filter(buyer=request.user).order_by('-priority')
    return render(request, 'buylist.html', {'gifts': gifts, 'show_user': True})


@login_required
def gift(request, userid, giftid):
    gift = get_object_or_404(Gift, pk=int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    return render(request, 'gift.html', {'gift': gift})


@login_required
def create(request):
    # If the form has been submitted...
    if request.method == 'POST':
        # A form bound to the POST data
        form = NewGift(request.POST)
        if form.is_valid():
            # All validation rules pass
            gift = form.save(commit=False)
            gift.owner = request.user
            gift.save()
            messages.success(request, _('Gift "%s" created.') % gift.title)
            # Redirect after POST
            return redirect('/%s/' % request.user.username)
        messages.error(request, _('Gift not created!'))
    else:
        # An unbound form
        form = NewGift()

    return render(request, 'create.html', {'form': form})


@login_required
def buy(request, userid, giftid):
    gift = get_object_or_404(Gift, pk=int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    gift.buy(request.user)
    messages.success(request, _('Gift "%s" marked as bought.') % gift.title)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def revoke(request, userid, giftid):
    gift = get_object_or_404(Gift, pk=int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    gift.revoke()
    messages.success(
        request, _('Gift "%s" no longer marked as bought.') % gift.title
    )
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete(request, userid, giftid):
    gift = get_object_or_404(Gift, pk=int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    title = gift.title
    gift.delete()
    messages.success(request, _('Gift "%s" deleted.') % title)
    return redirect('/')


@login_required
def edit(request, userid, giftid):
    gift = get_object_or_404(Gift, pk=int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    # If the form has been submitted...
    if request.method == 'POST':
        # A form bound to the POST data
        form = NewGift(request.POST, instance=gift)
        if form.is_valid():
            # All validation rules pass
            form.save()
            messages.success(request, _('Gift "%s" updated.') % gift.title)
            # Redirect after POST
            return redirect('/%s/' % request.user.username)
        messages.error(request, _('Gift not updated!'))
    else:
        # An unbound form
        form = NewGift(instance=gift)

    return render(request, 'edit.html', {'form': form, 'gift': gift})
