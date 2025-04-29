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
    fields = ('destino', 'data_ida', 'data_volta', 'valor', 'status', 'documentos_list')
    readonly_fields = ('documentos_list',)
    show_change_link = True

    def documentos_list(self, obj):
        if obj.id:
            documentos = obj.documentos_viagem.all()
            links = []

            for documento in documentos:
                url = documento.arquivo.url
                nome = documento.arquivo.name.split('/')[-1]
                tamanho_kb = documento.arquivo.size // 1024  # Tamanho em KB
                deletar_url = f"/admin/viagens/documentoviagem/{documento.id}/delete/"

                link_html = f"""
                    📎 <a href="{url}" target="_blank">{nome}</a> ({tamanho_kb} KB)
                    <a href="{deletar_url}" style="color:red; margin-left:10px;" target="_blank">[Excluir]</a>
                """
                links.append(link_html)

            add_url = f"/admin/viagens/documentoviagem/add/?viagem={obj.id}"
            links.append(f'<a class="button" href="{add_url}" target="_blank" style="margin-top:10px;">➕ Anexar Documento</a>')

            return mark_safe('<br><br>'.join(links))
        return "-"
    documentos_list.short_description = "Documentos"

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
