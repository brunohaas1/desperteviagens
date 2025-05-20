from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['home', 'cotacao', 'depoimentos', 'contato', 'sobre_nos', 'nossos_agentes', 'produtos']

    def location(self, item):
        return reverse(item)
