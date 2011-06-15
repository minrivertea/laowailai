# python
import os
import re
import logging
import md5, datetime
from time import time
import imghdr

# django
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext






try:
    from prowlpy import Prowl
    if settings.PROWL_API_KEY:
        prowl_api = Prowl(settings.PROWL_API_KEY)
    else:
        prowl_api = None
except ImportError:
    import warnings
    warnings.warn("prowlpy no installed")
    prowl_api = None


def prowlpy_wrapper(event, description="",
                    application="Laowailai",
                    priority=None):
    if not prowl_api:
        return
    
    params = dict(application=application,
                  event=event,
                  description=description
                  )
    
    if priority is not None:
        # An integer value ranging [-2, 2]: Very Low, Moderate, Normal, High, Emergency
        priority = int(priority)
        assert priority >= -2 and priority <= 2
        params['priority'] = priority
    
    def params2cachekey(params):
        s = []
        for v in params.values():
            if isinstance(v, basestring):
                s.append(v.encode('utf8'))
            else:
                s.append(str(v))
        s =  ''.join(s)[:256]
        return re.sub('\W','', s)
    
    cache_key = params2cachekey(params)
    
    if not cache.get(cache_key):
    
        try:
            prowl_api.post(**params)
        except:
            logging.error("Error sending event %r" % event, exc_info=True)
            
        cache.set(cache_key, time(), 10)
                        
