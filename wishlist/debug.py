'''
Wrapper to include useful information in error mails.
'''

from django.views.debug import SafeExceptionReporterFilter


class ExceptionReporterFilter(SafeExceptionReporterFilter):
    def get_request_repr(self, request):
        if request is None:
            return repr(None)

        result = super(ExceptionReporterFilter, self).get_request_repr(
            request
        )

        if (hasattr(request, 'session')
                and 'django_language' in request.session):
            lang = request.session['django_language']
        else:
            lang = None

        if (hasattr(request, 'user')
                and request.user.is_authenticated()):
            user = repr(request.user.username)
        else:
            user = None

        return '%s\n\nLanguage: %s\nUser: %s' % (
            result,
            lang,
            user,
        )
