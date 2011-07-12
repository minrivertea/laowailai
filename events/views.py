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
from laowailai.events.models import NewEvent
from laowailai.events.forms import AddEventForm
from laowailai.cities.models import City

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

def event(request, slug, id):
    city = get_object_or_404(City, slug=slug)
    event = get_object_or_404(NewEvent, pk=id)
    
    return render(request, "events/event.html", locals())
    
def events(request, slug):
    city = get_object_or_404(City, slug=slug)
    events = NewEvent.objects.filter(city=city).order_by('-start_date')

    return render(request, "events/events.html", locals())

@login_required    
def add_event(request, slug):
    city = get_object_or_404(City, slug=slug)
    laowai = request.user.get_profile()
    
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            date = datetime.strptime(form.cleaned_data['start_date'], '%m/%d/%Y')
            if form.cleaned_data['longitude']:
                longitude = form.cleaned_data['longitude']
                latitude = form.cleaned_data['latitude']
            else:
                longitude = 0
                latitude = 0
            creation_args = {
                        'title': form.cleaned_data['title'],
                        'description': form.cleaned_data['description'],
                        'start_date': date,
                        'location': form.cleaned_data['location'],
                        'owner': laowai,
                        'city': form.cleaned_data['city'],
                        'longitude': longitude,
                        'latitude': latitude,
            }
                     
            print creation_args
            event = NewEvent.objects.create(**creation_args)
            return render(request, "events/event.html", locals())
    
    else:
        form = AddEventForm()
    
    return render(request, "events/forms/add_event.html", locals())
    
    
    
    
    
    
    