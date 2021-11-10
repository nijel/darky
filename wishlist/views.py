from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth.models import User

from wishlist.models import Gift
from wishlist.forms import NewGift


@login_required
def overview(request):
    gifts = Gift.objects.filter(
        Q(private=False) | Q(buyer=request.user)
    ).order_by('owner', '-priority')
    return render(request, 'overview.html', {'gifts': gifts})


@login_required
def userlist(request, userid):
    user = get_object_or_404(User, username=userid)
    gifts = Gift.objects.filter(
        Q(private=False) | Q(buyer=request.user),
        owner=user
    ).order_by('-priority')
    return render(request, 'userlist.html', {'gifts': gifts, 'listuser': user})


@login_required
def buylist(request):
    gifts = Gift.objects.filter(buyer=request.user).order_by('-priority')
    return render(request, 'buylist.html', {'gifts': gifts, 'show_user': True})


@login_required
def gift(request, userid, giftid):
    obj = get_object_or_404(Gift, pk=int(giftid))
    if obj.owner.username != userid:
        raise Http404('User on gift do not match!')
    return render(request, 'gift.html', {'gift': obj})


@login_required
def create(request):
    if 'for' in request.GET and request.GET['for']:
        foruser = User.objects.get(username=request.GET['for'])
    elif 'for' in request.POST and request.POST['for']:
        foruser = User.objects.get(username=request.POST['for'])
    else:
        foruser = None
    # If the form has been submitted...
    if request.method == 'POST':
        # A form bound to the POST data
        form = NewGift(request.POST)
        if form.is_valid():
            # All validation rules pass
            obj = form.save(commit=False)
            if foruser:
                obj.private = True
                obj.buyer = request.user
                obj.owner = foruser
            else:
                obj.owner = request.user
            obj.save()
            messages.success(request, _('Gift "%s" created.') % obj.title)
            # Redirect after POST
            return redirect('/')
        messages.error(request, _('Gift not created!'))
    else:
        # An unbound form
        form = NewGift()

    return render(
        request,
        'create.html',
        {'form': form, 'foruser': foruser}
    )


@login_required
def buy(request, userid, giftid):
    obj = get_object_or_404(Gift, pk=int(giftid))
    if obj.owner.username != userid:
        raise Http404('User on gift do not match!')
    obj.buy(request.user)
    messages.success(request, _('Gift "%s" marked as bought.') % obj.title)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def revoke(request, userid, giftid):
    obj = get_object_or_404(Gift, pk=int(giftid))
    if obj.owner.username != userid:
        raise Http404('User on gift do not match!')
    obj.revoke()
    messages.success(
        request, _('Gift "%s" no longer marked as bought.') % obj.title
    )
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete(request, userid, giftid):
    obj = get_object_or_404(Gift, pk=int(giftid))
    if obj.owner.username != userid:
        raise Http404('User on gift do not match!')
    title = obj.title
    obj.delete()
    messages.success(request, _('Gift "%s" deleted.') % title)
    return redirect('/')


@login_required
def edit(request, userid, giftid):
    obj = get_object_or_404(Gift, pk=int(giftid))
    if obj.owner.username != userid:
        raise Http404('User on gift do not match!')
    # If the form has been submitted...
    if request.method == 'POST':
        # A form bound to the POST data
        form = NewGift(request.POST, instance=obj)
        if form.is_valid():
            # All validation rules pass
            form.save()
            messages.success(request, _('Gift "%s" updated.') % obj.title)
            # Redirect after POST
            return redirect('/')
        messages.error(request, _('Gift not updated!'))
    else:
        # An unbound form
        form = NewGift(instance=obj)

    return render(request, 'edit.html', {'form': form, 'gift': obj})
