from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'cotacao', 'depoimentos', 'contato', 'sobre_nos', 'nossos_agentes']

    def location(self, item):
        return reverse(item)
