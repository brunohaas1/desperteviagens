from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import SolicitacaoOrcamento, Cliente, Viagem, DocumentoViagem
from .forms import DocumentoViagemForm
from .admin_reports import relatorio_viagens
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import os
# Inline para múltiplos Documentos na Viagem
class DocumentoViagemInline(admin.TabularInline):
    model = DocumentoViagem
    form = DocumentoViagemForm
    extra = 1
    fields = ('viagem','arquivo',)

# Inline para Viagens dentro de Cliente


#class ViagemInline(admin.TabularInline):
 #   model = Viagem
 #   extra = 1
  #  fields = ('destino', 'data_ida', 'data_volta', 'valor', 'status', 'documentos_list')
 #  readonly_fields = ('documentos_list',)
  #  show_change_link = True

  #  def documentos_list(self, obj):
  #      if obj.id:
  #          documentos = obj.documentos_viagem.all()
  #          links = []
#
  #          for documento in documentos:
  #              url = documento.arquivo.url
  #              nome = documento.arquivo.name.split('/')[-1]
   #             tamanho_kb = documento.arquivo.size // 1024  # Tamanho em KB
  #              deletar_url = f"/admin/viagens/documentoviagem/{documento.id}/delete/"
#
  #              link_html = f"""
  #                  📎 <a href="{url}" target="_blank">{nome}</a> ({tamanho_kb} KB)
  #                  <a href="{deletar_url}" style="color:red; margin-left:10px;" target="_blank">[Excluir]</a>
   #             """
   #             links.append(link_html)

   #         add_url = f"/admin/viagens/documentoviagem/add/?viagem={obj.id}"
    #        links.append(f'<a class="button" href="{add_url}" target="_blank" style="margin-top:10px;">➕ Anexar Documento</a>')

   #         return mark_safe('<br><br>'.join(links))
   #     return "-"
   # documentos_list.short_description = "Documentos"


# Admin de Cliente (com Inline de Viagem)
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'cpf', 'email', 'telefone', 'celular', 'endereco', 'numero',
        'complemento', 'bairro', 'cep', 'cidade', 'uf', 'total_viagens', 'data_cadastro'
    )
    search_fields = ('nome', 'cpf', 'email', 'telefone', 'celular', 'endereco', 'cidade')
    list_filter = ('data_nascimento', 'data_cadastro', 'uf')
    
    def total_viagens(self, obj):
        return obj.viagem_set.count()
    total_viagens.short_description = 'Qtd. Viagens'

# Admin de Solicitação de Orçamento
@admin.register(SolicitacaoOrcamento)
class SolicitacaoOrcamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'destino', 'data_viagem', 'data_solicitacao')
    search_fields = ('nome', 'sobrenome', 'destino')
    list_filter = ('data_solicitacao',)

# Botão Relatórios no Admin
class RelatoriosAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        url = reverse('relatorio_viagens')
        return HttpResponseRedirect(url)

# DocumentoViagem também registrado manualmente
admin.site.register(DocumentoViagem)


