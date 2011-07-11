from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_was_posted
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

    
from laowailai.list.signals import new_laowai, new_subscriber #comment_notifier
from laowailai.cities.models import City



class Subscriber(models.Model):
    email = models.EmailField()
    date_added = models.DateTimeField('date_added', default=datetime.now)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.email
       

class Laowai(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    city = models.ForeignKey(City, blank=True, null=True)
    date_joined = models.DateTimeField('date added', default=datetime.now)
    subscribe = models.BooleanField(default=True)
    photo = models.ImageField(blank=True, upload_to='photos/profiles/')
    rank_points = models.IntegerField(default="0")
    profile_views = models.IntegerField(default="0")
    
    
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        return "http://www.laowailai.com/laowai/%s/" % self.id
    
    def get_liked_objects(self):
        liked_objects = Likes.objects.filter(liker=self.id)
        return liked_objects
     
    def get_posts(self):
        posts = Info.objects.filter(added_by=self)
        return posts
    
    def get_my_comments(self):
        posts = self.get_posts()
        comments = Comment.objects.filter(user_email=self.user.email)
        return comments
        
    def get_comments_about_me(self):
        comments = []
        posts = self.get_posts()
        for p in posts:
            for c in Comment.objects.all():
                if c.object_pk == str(p.id):
                    if c.user_name == self.name:
                        pass
                    else:
                        comments.append(c)    
        return comments
    
    def has_photo(self):
        if self.photo:
            return True
        else:
            return False   
    
    def added_places(self):
        from laowailai.places.models import Place
        places = Place.objects.filter(added_by=self)
        return places
    
    def added_questions(self):
        from laowailai.questions.models import Question
        questions = Question.objects.filter(added_by=self)
        return questions    

    def added_answers(self):
        from laowailai.questions.models import Answer
        answers = Answer.objects.filter(added_by=self)
        return answers 


class CommonInfo(models.Model):
    owner = models.ForeignKey(Laowai, null=True)
    date = models.DateTimeField('date added', default=datetime.now, null=True)
    city = models.ForeignKey(City, null=True)


class NewInfo(CommonInfo):
    content = models.TextField()
    
    def __unicode__(self):
        return self.content

    def get_like_count(self):
        from laowailai.list.models import Likes
        objects = Likes.objects.filter(liked=self.id)
        number = objects.count()
        return number

    def get_likers(self):
        from laowailai.list.models import Likes
        object_list = Likes.objects.filter(liked=self)
        likers = []
        for p in object_list:
            likers.append(p.liker)
        return likers
    
    def get_absolute_url(self):
        url = "/%s/feed/posts/%s/" % (self.city.slug, self.pk)
        # url = reverse('a_post', args=[(self.city.slug, self.pk)])
        return url      
    
        
class Info(models.Model):
    content = models.TextField()
    added_by = models.ForeignKey(Laowai)
    date_added = models.DateTimeField('date added', default=datetime.now)
    city = models.ForeignKey(City)    
    def __unicode__(self):
        return self.content
    

        

class Likes(models.Model):
   liker = models.ForeignKey(Laowai)
   liked = models.ForeignKey(Info)
   
#   def __unicode__(self):
#       return '%s likes %s' % self.liker, self.liked
      
    

class Suggestion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    votes = models.IntegerField()
    submitted_by = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added', default=datetime.now)
    
    def __unicode__(self):
        return self.title

#comment_was_posted.connect(comment_notifier, sender=Comment)


class Photo(models.Model):
    from laowailai.events.models import Event
    related_event = models.ForeignKey(Event, blank=True, null=True)
    related_info = models.ForeignKey(Info, blank=True, null=True)
    
    from laowailai.places.models import Place
    related_place = models.ForeignKey(Place, blank=True, null=True)
    photo = models.ImageField(upload_to="photos/photos")
    owner = models.ForeignKey(Laowai, related_name="random_photo")
    date_added = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.owner.name
        