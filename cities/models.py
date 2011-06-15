from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.template.loader import render_to_string

 
class City(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    chinese_name = models.CharField(max_length=200)
    description = models.TextField()
    centre_of_town = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name