from laowailai.cities.models import *
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    list_display = ('url', 'city', 'approved')

admin.site.register(City)
admin.site.register(Blog, BlogAdmin)





