from django.http import get_host

from django.conf import settings 

class MobileMiddleware(object):
    def process_request(self, request):
        host = get_host(request)
        if host and host.startswith('www.'):
            settings.TEMPLATE_DIRS = settings.MOBILE_TEMPLATE_DIRS
        else:
            settings.TEMPLATE_DIRS = settings.DESKTOP_TEMPLATE_DIRS