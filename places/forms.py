from django import forms
from django.forms import ModelForm

from django.forms.extras.widgets import SelectDateWidget

from laowailai.list.models import Laowai, Info, Subscriber
from laowailai.cities.models import City
from laowailai.places.models import CATEGORY_CHOICES
 
class AddPlaceForm(forms.Form):
    name = forms.CharField(max_length=200)
    chinese_name = forms.CharField(max_length=200)
    description = forms.CharField(required=True, widget=forms.Textarea)
    location = forms.CharField(max_length=200)
    longitude = forms.CharField(max_length=200)
    latitude = forms.CharField(max_length=200)
    city = forms.ModelChoiceField(queryset=City.objects.all())
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect)
    

class SearchForm(forms.Form):
    q = forms.CharField(label='Search')

class EditLocationForm(forms.Form):
    location = forms.CharField(max_length=200)
    longitude = forms.CharField(max_length=200)
    latitude = forms.CharField(max_length=200)    