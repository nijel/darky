'''
Messages generating code.
'''
from django.contrib import messages


def msg_ok(request, message):
    messages.success(request, message)


def msg_err(request, message):
    messages.error(request, message)

