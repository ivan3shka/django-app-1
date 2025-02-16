from django.contrib.sitemaps import Sitemap
from .models import Books

class ShopSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Books.objects.filter(created_at__isnull=False).order_by(
            '-created_at')

    def lastmod(self, obj: Books):
        return obj.created_at
