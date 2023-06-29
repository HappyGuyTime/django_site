from django.contrib.sitemaps import Sitemap
from .models import Product


class ShopSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Product.objects.filter(id__lte=5).order_by('-created_at')
    
    def lastmod(self, obj: Product):
        return obj.created_at
