from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.template.loader import render_to_string

from fuzhounet.list.models import Laowai
from fuzhounet.cities.models import City
from fuzhounet.places.models import Place



class Rating(models.Model):
    rated_object = models.ForeignKey(Place)
    rated_by = models.ForeignKey(Laowai)
    rating_score = models.IntegerField()
    date_rated = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.rated_object