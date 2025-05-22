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
    exportar_viagens_excel,
    exportar_viagens_pdf,
    exportar_clientes_pdf,
    exportar_clientes_excel,
    agenda_viagens,
    eventos_viagens,
    gerar_contrato_pdf,
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
    path('viagens/exportar-excel/', exportar_viagens_excel, name='exportar_viagens_excel'),
    path('viagens/exportar-pdf/', exportar_viagens_pdf, name='exportar_viagens_pdf'),
    path('clientes/exportar-pdf/', exportar_clientes_pdf, name='exportar_clientes_pdf'),
    path('clientes/exportar-excel/', exportar_clientes_excel, name='exportar_clientes_excel'),
    path("agenda/", agenda_viagens, name="agenda_viagens"),
    path("agenda/eventos/", eventos_viagens, name="eventos_viagens"),
    path("viagens/<int:viagem_id>/contrato/", gerar_contrato_pdf, name="gerar_contrato_pdf"),


]
