from django.db import models
from datetime import datetime


class BlogEntry(models.Model):
    slug = models.SlugField(max_length=80)
    promo_image = models.ImageField(upload_to='images/blog-photos')
    date_added = models.DateField(default=datetime.now)
    is_draft = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    content = models.TextField()
    
    def __unicode__(self):
        return self.slug
        
    def get_absolute_url(self):
        return "/blog/%s/" % self.slug # important! do not change (for feeds)
     
    def get_content(self):
        return self.summary
       
        
