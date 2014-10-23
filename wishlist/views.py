from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from wishlist.models import Gift
from wishlist.forms import NewGift

from wishlist.messages import msg_ok, msg_err


@login_required
def overview(request):
    gifts = Gift.objects.all().order_by('owner', '-priority')
    return render_to_response('overview.html', RequestContext(request, {'gifts': gifts}))


@login_required
def userlist(request, userid):
    user = get_object_or_404(User, username = userid)
    gifts = Gift.objects.filter(owner = user).order_by('-priority')
    return render_to_response('userlist.html', RequestContext(request, {'gifts': gifts, 'listuser': user}))


@login_required
def buylist(request):
    gifts = Gift.objects.filter(buyer = request.user).order_by('-priority')
    return render_to_response('buylist.html', RequestContext(request, {'gifts': gifts, 'show_user': True}))


@login_required
def gift(request, userid, giftid):
    gift = get_object_or_404(Gift, pk = int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    return render_to_response('gift.html', RequestContext(request, {'gift': gift}))


@login_required
def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewGift(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            gift = form.save(commit=False)
            gift.owner = request.user
            gift.save()
            msg_ok(request, _('Gift "%s" created.') % gift.title)
            return HttpResponseRedirect('/%s/' % request.user.username) # Redirect after POST
        msg_err(request, _('Gift not created!'))
    else:
        form = NewGift() # An unbound form

    return render_to_response('create.html', RequestContext(request,{'form': form }))


@login_required
def buy(request, userid, giftid):
    gift = get_object_or_404(Gift, pk = int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    gift.buy(request.user)
    msg_ok(request, _('Gift "%s" marked as bought.') % gift.title)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def revoke(request, userid, giftid):
    gift = get_object_or_404(Gift, pk = int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    gift.revoke()
    msg_ok(request, _('Gift "%s" no longer marked as bought.') % gift.title)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete(request, userid, giftid):
    gift = get_object_or_404(Gift, pk = int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    title = gift.title
    gift.delete()
    msg_ok(request, _('Gift "%s" deleted.') % title)
    return HttpResponseRedirect('/')


@login_required
def edit(request, userid, giftid):
    gift = get_object_or_404(Gift, pk = int(giftid))
    if gift.owner.username != userid:
        raise Http404('User on gift do not match!')
    if request.method == 'POST': # If the form has been submitted...
        form = NewGift(request.POST, instance = gift) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            msg_ok(request, _('Gift "%s" updated.') % gift.title)
            return HttpResponseRedirect('/%s/' % request.user.username) # Redirect after POST
        msg_err(request, _('Gift not updated!'))
    else:
        form = NewGift(instance = gift) # An unbound form

    return render_to_response('edit.html', RequestContext(request,{'form': form, 'gift': gift }))
