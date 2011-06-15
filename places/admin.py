from fuzhounet.places.models import *
from django.contrib import admin

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'city')

admin.site.register(Place, PlaceAdmin)





