from django import forms
from django.forms import ModelForm

from django.forms.extras.widgets import SelectDateWidget



from laowailai.list.models import Laowai, Info, Subscriber
from laowailai.cities.models import City

 
class AddEventForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(required=True, widget=forms.Textarea)
    start_date = forms.CharField(max_length=200)
    location = forms.CharField(max_length=200)
    city = forms.ModelChoiceField(queryset=City.objects.all())
    longitude = forms.CharField(max_length=200, required=False)
    latitude = forms.CharField(max_length=200, required=False)
