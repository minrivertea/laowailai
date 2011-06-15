from django.contrib.syndication.views import Feed
from list.models import Info

class LatestEntriesFeed(Feed):
    title = "LaoWaiLai Fuzhou Latest"
    link = "http://www.laowailai.com"
    description = "Latest news and posts about Fuzhou from LaoWaiLai.com"

    def items(self):
        return Info.objects.order_by('-date_added')[:10]

    def item_title(self, item):
        return "new post by %s" % item.added_by.name

    def item_description(self, item):
        return item.content
    
    def item_link(self, item):
        return item.get_absolute_url()
