from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from .models import Viagem, Cliente, DocumentoViagem
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class ViagensAdminSite(AdminSite):
    site_header = "Painel de Viagens"
    site_title = "Administração de Viagens"
    index_title = "Bem-vindo ao Sistema de Viagens"

    def each_context(self, request):
        context = super().each_context(request)
        context['site_logo'] = '/static/images/logo.png'  # 👈 Logo customizado
        return context

# Primeiro cria o painel
custom_admin_site = ViagensAdminSite(name='viagens_admin')

# Inline de Documentos dentro da Viagem
class DocumentoViagemInline(admin.TabularInline):
    model = DocumentoViagem
    extra = 1
    fields = ('arquivo',)
    show_change_link = False

# Inline de Viagens dentro do Cliente
class ViagemInline(admin.TabularInline):
    model = Viagem
    extra = 1
    fields = ('destino', 'data_ida', 'data_volta', 'valor', 'status')
    show_change_link = True

# Admin personalizado para Cliente
class ClienteAdminCustomizado(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email', 'telefone')
    search_fields = ('nome', 'cpf', 'email')
    list_filter = ('data_nascimento',)
    inlines = [ViagemInline]  # Aqui adicionamos Inline de Viagens dentro do Cliente!

# Admin personalizado para Viagem
class ViagemAdminCustomizado(admin.ModelAdmin):
    list_display = ('cliente', 'destino', 'data_ida', 'data_volta', 'status')
    search_fields = ('cliente__nome', 'destino')
    list_filter = ('data_ida', 'status')
    inlines = [DocumentoViagemInline]  # Aqui adicionamos Inline de Documentos dentro da Viagem!

# Registro dos dois no painel novo
custom_admin_site.register(Cliente, ClienteAdminCustomizado)
custom_admin_site.register(Viagem, ViagemAdminCustomizado)
