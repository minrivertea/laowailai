from django.conf import settings
from fuzhounet.list.models import Laowai, Info, Subscriber
from fuzhounet import settings
from django.shortcuts import get_object_or_404
from fuzhounet.cities.models import City

def common(request):
    from fuzhounet import settings
    ga_is_on = settings.GA_IS_ON
    return {'ga_is_on': ga_is_on}

def get_infos(request):
    try:
        laowai = get_object_or_404(Laowai, user=request.user)
    except:
        laowai = None
    infos = Info.objects.all().order_by('-date_added')[:10]
    objects = []
    for i in infos:
        if laowai:
            if laowai in i.get_likers():
                i_like = True
            else:
                i_like = False
        else:
            i_like = False    
        objects.append((i, i_like))
    
    return {'objects': objects}

def get_current_city(request):
    if request.user.is_authenticated():
        try:
            ref = request.session['CURRENTCITY']
            city = get_object_or_404(City, pk=ref)
        except:
            laowai = get_object_or_404(Laowai, user=request.user)
            city = laowai.city
        
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
    
    
    
