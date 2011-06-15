from django import forms

from laowailai.cities.models import City
 
class AddQuestionForm(forms.Form):
    question = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all())

    
class AddAnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)
    
class SearchForm(forms.Form):
    q = forms.CharField(label='Search')