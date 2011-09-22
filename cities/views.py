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
from laowailai.cities.models import City, Blog
from laowailai.events.models import NewEvent
from laowailai.utils import set_message

# django stuff
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from cities.forms import BlogAddForm
from list.models import Photo

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


def photos(request, slug):
    city = get_object_or_404(City, slug=slug)
    photos = Photo.objects.filter(city=city)
    return render(request, "cities/photos.html", locals())    

def add_blog(request, slug):
    city = get_object_or_404(City, slug=slug)
    
    if request.method == 'POST':
        form = BlogAddForm(request.POST)
        if form.is_valid():
            
            # check that this doesn't already exist...
            if Blog.objects.filter(url__icontains=form.cleaned_data['url']):
                pass
            
            else:
                newblog = Blog.objects.create(
                    url=form.cleaned_data['url'],
                    city=city,
                )
                
                newblog.feed = form.cleaned_data['feed']
                newblog.name = form.cleaned_data['name']
                
                newblog.save()
            
            message = "%s has been submitted to the %s blog roll and is awaiting approval. Thanks!" % (newblog.url, newblog.city)
            set_message(request, message)
            
            url = reverse('news_feed', args=[city.slug])
            return HttpResponseRedirect(url)
        
    else:
        form = BlogAddForm()
    

    return render(request, "cities/forms/add_blog_form.html", locals())
    
    
    