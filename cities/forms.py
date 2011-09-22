from django import forms


from laowailai.cities.models import City


 
class BlogAddForm(forms.Form):
    url = forms.URLField(required=True)
    feed = forms.URLField(required=False)
    name = forms.CharField(required=False)
