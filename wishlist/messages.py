'''
Messages generating code.
'''

def msg(request, msgtype, msgtext):
    message = '%s::%s' % (msgtype, msgtext)
    request.user.message_set.create(message = message)

def msg_ok(request, message):
    msg(request, 'success', message)

def msg_err(request, message):
    msg(request, 'error', message)

