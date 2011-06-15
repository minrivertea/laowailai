from django import forms
from django.forms import ModelForm

from django.forms.extras.widgets import SelectDateWidget



from fuzhounet.list.models import Laowai, Info, Subscriber

 
class AddEventForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(required=True, widget=forms.Textarea)
    start_date = forms.DateTimeField(widget=SelectDateWidget())
    end_date = forms.DateTimeField(widget=SelectDateWidget())
    location = forms.CharField(max_length=200)
