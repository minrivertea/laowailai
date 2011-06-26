from django.conf import settings
from laowailai.list.models import Laowai, Info, Subscriber
from django.shortcuts import get_object_or_404
from laowailai.cities.models import City

def common(request):
    from laowailai import settings
    ga_is_on = settings.GA_IS_ON
    sitename = settings.SITE_NAME
    return {'ga_is_on': ga_is_on, 'sitename': sitename}
    
def get_laowai(request):
    try:
        laowai = get_object_or_404(Laowai, user=request.user)
    except:
        laowai = None
    return {'laowai': laowai}
    
def get_latest_users(request):
    latest = Laowai.objects.all().order_by('-date_joined')
    return {'latest_users': latest}

def get_stats(request):
    subscribers = Subscriber.objects.all()
    signups = Laowai.objects.all()
    return {'subscribers': subscribers, 'signups': signups}
    
    
    
