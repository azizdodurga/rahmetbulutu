from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"  # Google'a ne sıklıkla kontrol etmesi gerektiğini söyler
    priority = 0.9        # 0.0 ile 1.0 arası öncelik değeri

    def items(self):
        return Post.objects.all().order_by('-created_on')

    def lastmod(self, obj):
        return obj.created_on # En son ne zaman güncellendiğini belirtir

    def location(self, obj):
        # Post modelinde get_absolute_url metodun varsa burası otomatik çalışır. 
        # Yoksa: return f'/post/{obj.slug}/'
        return obj.get_absolute_url()