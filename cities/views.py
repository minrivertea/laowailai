# core python imports
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import timedelta, datetime
from PIL import Image
from cStringIO import StringIO
import os, md5
import smtplib

# stuff from my app
from laowailai.list.models import Laowai
from laowailai.cities.models import City
from laowailai.events.models import NewEvent

# django stuff
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf




#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )

def cities(request):
    cities = City.objects.all().order_by('name')
    return render(request, "cities/cities.html", locals())


def city(request, slug):
    city = get_object_or_404(City, slug=slug)
    url = reverse("news_feed", args=[city.slug])
    return HttpResponseRedirect(url)

def mark_city(request, id):
    city = get_object_or_404(City, pk=id) 
    laowai = request.user.get_profile()
    laowai.cities.add(city)
    laowai.city = city
    laowai.save()
    url = reverse('city', args=[city.slug])
    return HttpResponseRedirect(url)
    
    
    
    
    