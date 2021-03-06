from laowailai.list.models import *
from django.contrib import admin

class NewInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'city', 'content')
    
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'city', 'date')

admin.site.register(Likes)
admin.site.register(NewInfo, NewInfoAdmin)
#admin.site.register(CommonInfo)
admin.site.register(Laowai)
admin.site.register(Subscriber)
admin.site.register(Suggestion)
admin.site.register(Photo, PhotoAdmin)




