from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.template.loader import render_to_string

from fuzhounet.list.models import Laowai
from fuzhounet.cities.models import City
 
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField('date added', default=datetime.now)
    start_date = models.DateField('date added')
    added_by = models.ForeignKey(Laowai)
    location = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    city = models.ForeignKey(City)
    
    def __unicode__(self):
        return self.title