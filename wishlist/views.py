from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.utils.translation import ugettext as _

from wishlist.models import Gift
from wishlist.forms import NewGift

from wishlist.messages import msg_ok, msg_err

def overview(request):
    return render_to_response('overview.html')

def gift(request, giftid):
    gift = get_object_or_404(Gift, pk = int(giftid))
    return render_to_response('gift.html', {'gift': gift})

def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewGift(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            msg_ok(request, _('Gift created'))
            return HttpResponseRedirect('/') # Redirect after POST
        msg_err(request, _('Gift not created!'))
    else:
        form = NewGift() # An unbound form

    return render_to_response('create.html', {
        'form': form,
    })
