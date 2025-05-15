from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from .models import Viagem, Cliente, DocumentoViagem
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.shortcuts import redirect
from urllib.parse import quote


class DocumentoViagemAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return super().response_add(request, obj, post_url_continue)

    def response_delete(self, request, obj_display, obj_id):
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return super().response_delete(request, obj_display, obj_id)

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

            # URL para voltar após adicionar/excluir
            referer_url = quote(f"/painel-viagens/viagens/cliente/{obj.cliente.id}/change/")

            for documento in documentos:
                url = documento.arquivo.url
                nome = documento.arquivo.name.split('/')[-1]
                tamanho_kb = documento.arquivo.size // 1024
                deletar_url = reverse("viagens_admin:viagens_documentoviagem_delete", args=[documento.id])
                deletar_url += f"?next={referer_url}"

                link_html = f"""
                    📎 <a href="{url}" target="_blank">{nome}</a> ({tamanho_kb} KB)
                    <a href="{deletar_url}" style="color:red; margin-left:10px;" target="_blank">[Excluir]</a>
                """
                links.append(link_html)

            add_url = reverse("viagens_admin:viagens_documentoviagem_add") + f"?viagem={obj.id}&next={referer_url}"
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
#custom_admin_site.register(Viagem, ViagemAdminCustomizado)
custom_admin_site.register(DocumentoViagem, DocumentoViagemAdmin)