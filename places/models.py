from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.template.loader import render_to_string

from laowailai.list.models import Laowai, CommonInfo
from laowailai.cities.models import City

#these are the values in the database
CATEGORY_1 = 'eat'
CATEGORY_2 = 'drink'
CATEGORY_3 = 'do'
CATEGORY_4 = 'see'
CATEGORY_5 = 'buy'
# these are the values it will display
CATEGORY_CHOICES = (
            (CATEGORY_1, u"Somewhere to eat"),
            (CATEGORY_2, u"Somewhere to drink"),
            (CATEGORY_3, u"Something to do"),
            (CATEGORY_4, u"Something to see"),
            (CATEGORY_5, u"Somewhere to shop"),     
)
 
class NewPlace(CommonInfo):
    name = models.CharField(max_length=200)
    chinese_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    rating_count = models.IntegerField(default="0")
    rating_total = models.IntegerField(default="0")
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)


class Place(models.Model):
    name = models.CharField(max_length=200)
    chinese_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    city = models.ForeignKey(City)
    added_by = models.ForeignKey(Laowai)
    date_added = models.DateTimeField(default=datetime.now())
    rating_count = models.IntegerField(default="0")
    rating_total = models.IntegerField(default="0")
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    
    def __unicode__(self):
        return self.name
    
    def get_average_rating(self):
        if self.rating_count > 0:
            average = (self.rating_total/self.rating_count)
        else:
            average = "0"
        return average
        
    def get_current_rating(self):
        if self.rating_count > 0:
            current_rating = self.get_average_rating() * 18
        else:
            current_rating = 0
        return current_rating  
    
    def canonical_url(self):
        return "http://www.laowailai.com/places/%s/%s" % (self.city.slug, self.slug)
    
    def has_map(self):
        if self.longitude == None or self.latitude == None:
            return False
        else:
            return True
    
    def get_absolute_url(self):
        return "/places/%s/" % self.pk  
        
    def get_photos(self):
        from laowailai.list.models import Photo
        photos = Photo.objects.filter(related_place=self.id)
        return photos   