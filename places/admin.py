from laowailai.places.models import *
from django.contrib import admin

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'city')

class NewPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'city')

admin.site.register(Place, PlaceAdmin)
admin.site.register(NewPlace, NewPlaceAdmin)





