from django.contrib.syndication.feeds import Feed
from minriver.blog.models import BlogEntry

class LatestEntries(Feed):
    title = "Chinese tea blog from the Min River Tea Farm"
    link = "/"
    description = "News and info about Chinese tea and our Chinese tea products."

    def items(self):
        return BlogEntry.objects.order_by('-date_added')[:5]





