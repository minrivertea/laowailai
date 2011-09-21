from django.db import models
from datetime import datetime

from string import Template
from django.db import connection
from django.conf import settings


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



class DistanceManager(models.Manager):

    def nearest_to(self, point, number=20, within_range=None, offset=0,
                   exclude=None, extra_where_sql=''):
                   
        if not isinstance(point, tuple):
            raise TypeError
       
        cursor = connection.cursor()
        x, y = point # x=latitude, y=longitude
        table = self.model._meta.db_table
        print exclude
        
        
        template = Template("""
            SELECT 
            slug,
            ATAN2(
                SQRT(
                POW(COS(RADIANS($y)) *
                    SIN(RADIANS(gl.latitude - $x)), 2) +
                POW(COS(RADIANS(gl.longitude)) * SIN(RADIANS($y)) -
                    SIN(RADIANS(gl.longitude)) * COS(RADIANS($y)) * 
                    COS(RADIANS(gl.latitude - $x)), 2)), 
                (SIN(RADIANS(gl.longitude)) * SIN(RADIANS($y)) + 
                COS(RADIANS(gl.longitude)) * COS(RADIANS($y)) * 
                COS(RADIANS(gl.latitude - $x)))
                ) * 6372.795 AS distance
            FROM 
            $table gl
            
            WHERE NOT gl.slug = '%s' AND NOT gl.latitude = ''
            ORDER BY distance ASC
            LIMIT $number
            OFFSET $offset
            ;
        """ % (exclude,))
       

        sql_string = template.substitute(locals())
          
        cursor.execute(sql_string)
        nearbys = cursor.fetchall()

        nearbys_reduced = []
        # filter out the results that are outside the range
        for p in nearbys:
            if p[1] < int(within_range):
                nearbys_reduced.append(p)

               
        # get a list of primary keys of the nearby model objects
        slugs = [p[0] for p in nearbys_reduced]
        
        # get a list of distances from the model objects
        dists = [p[1] for p in nearbys_reduced]
        
        places = self.filter(slug__in=slugs).select_related()
        
        # the QuerySet comes back in an undefined order; let's
        # order it by distance from the given point
        
        def order_by(objects, listing, name):
            """a convenience method that takes a list of objects,
            and orders them by comparing an attribute given by `name`
            to a sorted listing of values of the same length."""
            sorted = []
            for i in listing:
                for obj in objects:
                    if getattr(obj, name) == i:
                        sorted.append(obj)
            return sorted
        
        return zip(order_by(places, slugs, 'slug'), dists)
    
   
    



 
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
    # verified = models.IntegerField(default="0")
    
    objects = DistanceManager()

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
        photos = Photo.objects.filter(object_pk=self.id)
        return photos
    
    def get_nearest(self, num=5, within_range=20):
        r = []
        places = NewPlace.objects.nearest_to((self.latitude, self.longitude),
                                                number=num, within_range=within_range,
                                                exclude=self.slug)
        
        for place, distance_miles in places:
            place.distance_miles = distance_miles
            r.append(place)
        
        return r   

# this is depracated, DO NOT USE
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