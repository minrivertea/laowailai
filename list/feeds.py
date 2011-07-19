from django.contrib.syndication.views import Feed
from places.models import NewPlace

class LatestEntriesFeed(Feed):
    title = "Latest places in China from www.laowailai.com"
    link = "http://www.laowailai.com"
    description = "Latest places in China from LaoWaiLai.com"

    def items(self):
        return NewPlace.objects.order_by('-date_added')[:10]

    def item_title(self, item):
        return "new post by %s" % item.added_by.name

    def item_description(self, item):
        return item.content
    
    def item_link(self, item):
        return item.get_absolute_url()
