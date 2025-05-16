from django.urls import path
from . import views
from .admin_reports import relatorio_viagens
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('', views.home, name='home'),
    path('cotacao/', views.cotacao, name='cotacao'),
    path('depoimentos/', views.depoimentos, name='depoimentos'),
    path('produtos/', views.produtos, name='produtos'),
    path('orcamento/sucesso/', views.orcamento_sucesso, name='orcamento_sucesso'),
    path('contato/', views.contato, name='contato'),
    path('relatorios/viagens/', relatorio_viagens, name='relatorio_viagens'),
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('nossos-agentes/', views.nossos_agentes, name='nossos_agentes'),
    path('produtos/', views.produtos, name='produtos'),
]