from django.contrib.sitemaps import Sitemap
from westiseast.blog.models import BlogEntry

class BlogEntrySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return BlogEntry.objects.filter(is_draft=False)

    def lastmod(self, obj):
        return obj.date_added
        
    def location(self, obj):
        return "/blog/%s/" % obj.slug


