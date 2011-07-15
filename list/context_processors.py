from django.conf import settings
from laowailai.list.models import Laowai, Info, Subscriber
from django.shortcuts import get_object_or_404
from laowailai.cities.models import City
from laowailai.places.models import NewPlace
from notification.models import Notice

def common(request):
    from laowailai import settings
    context = {}
    context['sitename'] = settings.SITE_NAME
    context['ga_is_on'] = settings.GA_IS_ON
    context['all_cities'] = City.objects.all()
    if request.user.is_authenticated():
        context['notifications'] = Notice.objects.filter(recipient=request.user, unseen=True)
        if request.user.get_profile().city:
            context['city'] = request.user.get_profile().city
    return context
    
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
    signups = Laowai.objects.count()
    places = NewPlace.objects.count()
    return {'places': places, 'signups': signups}
    
    
    
