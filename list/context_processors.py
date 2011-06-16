from django.conf import settings
from laowailai.list.models import Laowai, Info, Subscriber
from django.shortcuts import get_object_or_404
from laowailai.cities.models import City

def common(request):
    from laowailai import settings
    ga_is_on = settings.GA_IS_ON
    return {'ga_is_on': ga_is_on}

def get_current_city(request):
    try:
        city = get_object_or_404(City, pk=request.session['CURRENTCITY'])
    except:
        if request.user.is_authenticated():
            laowai = get_object_or_404(Laowai, user=request.user)
            if laowai.city:
                city = laowai.city
            else:
                city = get_object_or_404(City, pk="1")
        else:
            city = get_object_or_404(City, slug="china")
        
    return {'current_city': city}
    
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
    
    
    
