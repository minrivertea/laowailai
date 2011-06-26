# core python imports
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import timedelta, datetime
from PIL import Image
from cStringIO import StringIO
import os, md5
import smtplib
import re

# stuff from my app
from laowailai.list.models import Laowai
from laowailai.places.models import Place
from laowailai.places.forms import AddPlaceForm, SearchForm, EditLocationForm
from laowailai.places.data import find_places
from laowailai.slugify import get_slugify
from laowailai.ratings.models import Rating
from laowailai.cities.models import City

# django stuff
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.core import serializers

from django.core.serializers.json import DjangoJSONEncoder



#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )

def places(request, slug, category=None, qs=None, parameters={}):
    
    city = get_object_or_404(City, slug=slug)
    if city.slug == "china":
        places = Place.objects.all()
    else:
        places = Place.objects.filter(city=city).order_by('?')
    
    # if there's a search query
    if request.GET.get('q'):
        search_form = SearchForm(initial=request.GET)
        q = request.GET.get('q')
        places = find_places(q=q, qs=qs, city=city, **parameters)
        return render(request, "places/places.html", locals())
    else:
        search_form = SearchForm()
        
    # if there's an AJAX request to filter the results:
    if request.GET.get('xhr'):
        if request.GET.get('filter') == 'recent':
            new_list = []
            if request.GET.get('category'):
                new_list.append(render_to_string('places/snippets/place-list.html', {
                    'places': places.filter(category=request.GET.get('category')).order_by('-date_added'),
                }
                ))
            else:
                new_list.append(render_to_string('places/snippets/place-list.html', 
                    {'places': places.order_by('-date_added')}
                ))
            json =  simplejson.dumps(new_list, cls=DjangoJSONEncoder)
            return HttpResponse(json, mimetype='application/json')
        
        elif request.GET.get('filter') == 'highest':
            if request.GET.get('category'):
                places = places.filter(category=request.GET.get('category'))
            data = sorted(places, reverse=True, key=lambda x: x.get_current_rating())
            new_list = []
            new_list.append(render_to_string('places/snippets/place-list.html', {'places': data}))
            json =  simplejson.dumps(new_list, cls=DjangoJSONEncoder)
            return HttpResponse(json, mimetype='application/json')
    
            
    from laowailai.places.models import CATEGORY_CHOICES
    categories = CATEGORY_CHOICES
    
    # if there's filters, apply them to the queryset
    if request.GET.get('category'):
        places = places.filter(
            category=request.GET.get('category'),
            city=city).order_by('-date_added').order_by('?')
        selected = request.GET.get('category')
    
    # if there's a filter, filter the results
    if request.GET.get('filter'):
        selected = request.GET.get('filter')
        if request.GET.get('filter') == "recent":
            places = places.order_by('-date_added')[:10] 
        elif request.GET.get('filter') == 'highest':
            places_list = []
            for place in places:
                places_list.append(dict(
                    place=place,
                    id=place.id,
                    name=place.name,
                    get_current_rating=place.get_current_rating(),
                    rating_count=place.rating_count,
                ))
            places = sorted(places_list, reverse=True, key=lambda k: k['get_current_rating'])[:10]

    return render(request, "places/places.html", locals())

def place(request, slug, id):
    city = get_object_or_404(City, slug=slug)
    
    place = get_object_or_404(Place, pk=id)
    try:
        laowai = get_object_or_404(Laowai, user=request.user)
    except:
        laowai = None
    # check if this has been rated
    if place.rating_count > 0:
        # get a list of ratings related to this place and this user
        rated = Rating.objects.filter(rated_object=place, rated_by=laowai)
    
    if place.get_average_rating > 0:
        current_rating = int(place.get_average_rating()) * 25
    else:
        current_rating = 0
    return render(request, "places/place.html", locals())

@login_required
def add_place(request, slug):
    city = get_object_or_404(City, slug=slug)
    
    if request.method == 'POST':
        form = AddPlaceForm(request.POST)
        if form.is_valid():
            laowai = get_object_or_404(Laowai, user=request.user)
            slug = get_slugify(form.cleaned_data['name'])
            while(Place.objects.filter(slug__iexact=slug).count()):
                current_number_suffix_match = re.search("\d+$", slug)
                current_number_suffix = current_number_suffix_match and current_number_suffix_match.group() or 0
                next = str(int(current_number_suffix) +1)
                slug = re.sub("(\d+)?$", next, slug)
            creation_args = {
                        'name': form.cleaned_data['name'],
                        'chinese_name': form.cleaned_data['chinese_name'],
                        'description': form.cleaned_data['description'],
                        'location': form.cleaned_data['location'],
                        'city': form.cleaned_data['city'],
                        'added_by': laowai,
                        'slug': slug,
                        'category': form.cleaned_data['category'],
                        'longitude': form.cleaned_data['longitude'],
                        'latitude': form.cleaned_data['latitude'],
            }
                   
            
            place = Place.objects.create(**creation_args)
            redirect_url = reverse('places', args=[city.slug])
            return HttpResponseRedirect(redirect_url)
    
    else:
        form = AddPlaceForm()
        
    return render(request, "places/forms/add_place.html", locals())

@login_required
def edit_location(request, id):
    place = get_object_or_404(Place, pk=id)
    
    # just double check that someone isn't trying to edit a place with an existing location
    if place.longitude or place.latitude:
        return Http404
    if request.method == 'POST':
        form = EditLocationForm(request.POST)
        if form.is_valid():
            place.location = form.cleaned_data['location']
            place.longitude = form.cleaned_data['longitude']
            place.latitude = form.cleaned_data['latitude']
            place.save()
                    
            redirect_url = reverse('place', args=[place.id])
            return HttpResponseRedirect(redirect_url)
            
    
    else:
        form = EditLocationForm()
        
    return render(request, "places/forms/edit_location.html", locals())    

@login_required
def add_rating(request, place, value):
    place = get_object_or_404(Place, pk=place)
    place.rating_count += 1
    place.rating_total += int(value)
    place.save()
    
    laowai = get_object_or_404(Laowai, user=request.user)
    rating = Rating.objects.create(
        rated_object = place,
        rated_by = laowai,
        rating_score = value,
    )
    
    rating.save()
    
    url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(url)

def get_place_by_slug(request, city, slug):
    city = get_object_or_404(City, slug=city)
    place = get_object_or_404(Place, slug=slug)
    request.session['CURRENTCITY'] = city.id
    
    url = reverse('place', args=[place.id])
    return HttpResponseRedirect(url)
    
    
    
    
    
         
