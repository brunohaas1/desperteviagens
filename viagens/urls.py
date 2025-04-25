from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cotacao/', views.cotacao, name='cotacao'),
    path('depoimentos/', views.depoimentos, name='depoimentos'),
    path('produtos/', views.produtos, name='produtos'),
    path('orcamento/sucesso/', views.orcamento_sucesso, name='orcamento_sucesso'),
    path('contato/', views.contato, name='contato'),
]