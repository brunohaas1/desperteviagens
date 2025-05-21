from django.urls import path
from .views import (
    dashboard_admin,
    lista_clientes,
    lista_documentos,
    delete_documento,
    lista_viagens,
    adicionar_cliente,
    adicionar_viagem,
    adicionar_documento,

)

urlpatterns = [
    path("", dashboard_admin, name="dashboard_admin"),
    path("clientes/", lista_clientes, name="lista_clientes"),
    path('viagens/', lista_viagens, name="lista_viagens"),
    path("documentos/", lista_documentos, name="lista_documentos"),
    path("documentos/delete/<int:doc_id>/", delete_documento, name="delete_documento"),
    path("clientes/adicionar/", adicionar_cliente, name="adicionar_cliente"),
    path("clientes/<int:cliente_id>/adicionar-viagem/", adicionar_viagem, name="adicionar_viagem"),
    path("viagens/<int:viagem_id>/anexar-documento/", adicionar_documento, name="adicionar_documento"),



]
