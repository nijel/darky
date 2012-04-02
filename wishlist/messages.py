'''
Messages generating code.
'''
from django.contrib import messages

def msg(request, msgtype, msgtext):
    message = '%s::%s' % (msgtype, msgtext)
    messages.info(request, message)

def msg_ok(request, message):
    msg(request, 'success', message)

def msg_err(request, message):
    msg(request, 'error', message)

