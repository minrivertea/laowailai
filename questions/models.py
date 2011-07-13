from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.template.loader import render_to_string

from laowailai.list.models import Laowai, CommonInfo
from laowailai.cities.models import City

from smart_slug.fields import SmartSlugField


class NewQuestionManager(models.Manager):
    def filter(self):
        qs = super(QuestionManager, self).get_query_set()
        return qs.filter()

class NewQuestion(CommonInfo):
    question = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200)
    vote_count = models.IntegerField(default="0")
    is_published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.question     

    def get_absolute_url(self):
        return "/%s/questions/%s/" % (self.city, self.slug)
    
    def answers_count(self):
        answers = Answer.objects.filter(question=self)
        return answers.count() 

# deprecated, can delete this when I get the time... 
class Question(models.Model):
    question = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200)
    city = models.ForeignKey(City)
    added_by = models.ForeignKey(Laowai)
    date_added = models.DateTimeField(default=datetime.now())
    vote_count = models.IntegerField(default="0")
    is_published = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.question 
    
        
class Answer(models.Model):
    question = models.ForeignKey(NewQuestion)
    added_by = models.ForeignKey(Laowai)
    answer = models.TextField()
    date_added = models.DateTimeField(default=datetime.now())
    vote_count = models.IntegerField(default="0")
    is_published = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "%s, %s" % (self.added_by, self.answer)      

class Vote(models.Model):
    answer = models.ForeignKey(Answer)
    laowai = models.ForeignKey(Laowai)
    
    def __unicode__(self):
        return self.answer.answer