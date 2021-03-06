from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget


from laowailai.cities.models import City
from laowailai.list.models import Laowai, Info, Subscriber

 
class SubscriberAddForm(forms.Form):
    email = forms.EmailField(required=True)

          
class InfoAddForm(forms.Form):
    content = forms.CharField(required=False, widget=forms.Textarea)
    city = forms.ModelChoiceField(queryset=City.objects.all())
    image = forms.ImageField(required=False)
    
        
class UnsubscribeForm(forms.Form):
    email = forms.EmailField(required=True)  
    
class SubscribeForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=200, required=False)
    receive_emails = forms.BooleanField()   
    
class ProfilePhotoUploadForm(forms.Form):
    photo = forms.ImageField()


class TellAFriendForm(forms.Form):
    recipient = forms.EmailField(required=True)
    sender = forms.EmailField(required=True)
    message = forms.CharField(required=False, widget=forms.Textarea)
    
class AddBioForm(forms.Form):
    bio = forms.CharField(required=True, widget=forms.Textarea)
    
class SuggestionForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    
    
    
    
        