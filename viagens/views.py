from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template.loader import get_template
from django.conf import settings
from django_select2.views import AutoResponseView
from docxtpl import DocxTemplate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from xhtml2pdf import pisa
import openpyxl
import os
from django.utils.timezone import localtime, now
import pandas as pd
from datetime import timedelta
from pathlib import Path
from django.http import JsonResponse
from .models import Cliente, Viagem, DocumentoViagem
from .forms import (
    SolicitacaoOrcamentoForm, ClienteForm, ViagemForm, DocumentoViagemForm
)

# Páginas públicas
def home(request):
    return render(request, 'viagens/html/home.html')

def cotacao(request):
    if request.method == 'POST':
        form = SolicitacaoOrcamentoForm(request.POST)
        if form.is_valid():
            orcamento = form.save()
            mensagem = f"""
📩 Nova solicitação de orçamento:

Nome: {orcamento.nome} {orcamento.sobrenome}
Email: {orcamento.email}
Telefone: {orcamento.telefone}
Destino: {orcamento.destino}
Data da viagem: {orcamento.data_viagem.strftime('%d/%m/%Y')}
"""
            send_mail('Nova solicitação de orçamento', mensagem, None, ['desperteviagens@gmail.com'])
            return redirect('orcamento_sucesso')
    else:
        form = SolicitacaoOrcamentoForm()
    return render(request, 'viagens/html/cotacao.html', {'form': form})

def depoimentos(request):
    return render(request, 'viagens/html/depoimentos.html')

def produtos(request):
    return render(request, 'viagens/html/produtos.html')

def orcamento_sucesso(request):
    return render(request, 'viagens/html/orcamento_sucesso.html')

def contato(request):
    return render(request, 'viagens/html/contato.html')

def sobre_nos(request):
    return render(request, 'viagens/html/sobre_nos.html')

def nossos_agentes(request):
    return render(request, 'viagens/html/nossos_agentes.html')

# Painel administrativo
@staff_member_required
def dashboard_admin(request):
    hoje = now()
    mes_atual, ano_atual = hoje.month, hoje.year

    faturamento_mes = Viagem.objects.filter(
        data_ida__month=mes_atual,
        data_ida__year=ano_atual
    ).aggregate(total=Sum("valor"))['total'] or 0

    proximas_viagens = Viagem.objects.filter(
        data_ida__gte=hoje,
        data_ida__lte=hoje + timedelta(days=7)
    ).order_by("data_ida")

    context = {
        'total_clientes': Cliente.objects.count(),
        'total_viagens': Viagem.objects.count(),
        'total_documentos': DocumentoViagem.objects.count(),
        'faturamento_mes': faturamento_mes,
        'proximas_viagens': proximas_viagens,
    }
    return render(request, 'viagens/painel/dashboard.html', context)

def lista_clientes(request):
    busca = request.GET.get("busca")
    clientes = Cliente.objects.all()
    if busca:
        clientes = clientes.filter(Q(nome__icontains=busca) | Q(cpf__icontains=busca))
    return render(request, "viagens/painel/clientes.html", {"clientes": clientes, "busca": busca})

def lista_viagens(request):
    status = request.GET.get("status")
    cliente_nome = request.GET.get("cliente_nome")

    viagens = Viagem.objects.all()
    if status:
        viagens = viagens.filter(status=status)
    if cliente_nome:
        viagens = viagens.filter(clientes__nome__icontains=cliente_nome)

    clientes = Cliente.objects.all()
    return render(request, "viagens/painel/viagens.html", {
        "viagens": viagens,
        "clientes": clientes,
        "status_ativo": status,
        "cliente_ativo": cliente_nome
    })

def lista_documentos(request):
    documentos = DocumentoViagem.objects.select_related("viagem").all().order_by("-id")
    return render(request, "viagens/painel/documentos.html", {"documentos": documentos})

@require_POST
def delete_documento(request, doc_id):
    get_object_or_404(DocumentoViagem, id=doc_id).delete()
    return redirect("painel:lista_viagens")

def adicionar_cliente(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("painel:lista_clientes")
    return render(request, "viagens/painel/adicionar_cliente.html", {"form": form})

def adicionar_viagem(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    form = ViagemForm(request.POST or None)
    if form.is_valid():
        viagem = form.save()
        viagem.clientes.add(cliente)
        return redirect("painel:lista_clientes")
    return render(request, "viagens/painel/adicionar_viagem.html", {"form": form, "cliente": cliente})

def adicionar_documento(request, viagem_id):
    viagem = get_object_or_404(Viagem, id=viagem_id)
    form = DocumentoViagemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        doc = form.save(commit=False)
        doc.viagem = viagem
        doc.save()
        return redirect("painel:lista_viagens")
    return render(request, "viagens/painel/adicionar_documento.html", {"form": form, "viagem": viagem})

def exportar_viagens_excel(request):
    wb, ws = openpyxl.Workbook(), openpyxl.Workbook().active
    ws.title = "Viagens"
    ws.append(['Clientes', 'Destino', 'Data Ida', 'Data Volta', 'Valor', 'Status'])
    for v in Viagem.objects.all():
        nomes = ", ".join([c.nome for c in v.clientes.all()])
        ws.append([nomes, v.destino, v.data_ida.strftime('%d/%m/%Y'), v.data_volta.strftime('%d/%m/%Y'), f"{v.valor:.2f}", v.status])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=relatorio_viagens.xlsx'
    wb.save(response)
    return response

def exportar_viagens_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_viagens.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Relatório de Viagens")
    p.setFont("Helvetica", 10)
    y = height - 100

    viagens = Viagem.objects.all()

    for v in viagens:
        if y < 60:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 50

        nomes = ", ".join([c.nome for c in v.clientes.all()])
        p.drawString(40, y, nomes[:35])
        p.drawString(230, y, v.destino[:25])
        p.drawString(320, y, v.data_ida.strftime('%d/%m/%Y'))
        p.drawString(390, y, v.data_volta.strftime('%d/%m/%Y'))
        p.drawString(450, y, f"R$ {v.valor:.2f}")
        p.drawString(530, y, v.status)

        y -= 20

    p.showPage()
    p.save()

    return response

def eventos_viagens(request):
    eventos = []
    for v in Viagem.objects.all():
        nomes = ", ".join([c.nome for c in v.clientes.all()])
        eventos.append({"title": f"{nomes} - {v.destino}", "start": v.data_ida.isoformat(), "end": v.data_volta.isoformat()})
    return JsonResponse(eventos, safe=False)

def exportar_clientes_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_clientes.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Relatório de Clientes")

    p.setFont("Helvetica", 10)
    y = height - 100

    for c in Cliente.objects.all():
        if y < 60:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 50
        p.drawString(40, y, c.nome[:35])      # 35 caracteres
        p.drawString(250, y, c.cpf or "-")   
        p.drawString(350, y, c.email[:30] or "-")
        p.drawString(500, y, c.telefone or "-")
        y -= 20

    p.showPage()
    p.save()

    return response

def exportar_clientes_excel(request):
    df = pd.DataFrame(Cliente.objects.all().values("nome", "cpf", "email", "telefone", "data_nascimento"))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=relatorio_clientes.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Clientes')
    return response

def link_callback(uri, rel):
    return os.path.join(settings.BASE_DIR, uri.replace(settings.STATIC_URL, "static/"))

def gerar_contrato_docx(request, cliente_id, viagem_id):
    cliente = Cliente.objects.get(id=cliente_id)
    viagem = Viagem.objects.get(id=viagem_id)
    meses = {
    1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
    5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
    9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
}
    hoje = localtime(now())
    mes_por_extenso = meses[hoje.month]  
    # Caminho para o template .docx
    template_path = os.path.join(settings.BASE_DIR, 'templates', 'viagens', 'contratos', 'contrato_template.docx')

    doc = DocxTemplate(template_path)

    context = {
        'cliente': cliente,
        'viagem': viagem,
        'hoje': hoje,
        'mes_por_extenso': mes_por_extenso,
    }

    doc.render(context)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=contrato_preenchido.docx'

    doc.save(response)

    return response
def buscar_clientes(request):
    termo = request.GET.get("q", "")
    clientes = Cliente.objects.filter(nome__icontains=termo)[:10]
    resultados = [{"id": cliente.id, "text": cliente.nome} for cliente in clientes]
    return JsonResponse({"results": resultados})
    
@staff_member_required
def agenda_viagens(request):
    return render(request, "viagens/painel/agenda.html")

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("painel:lista_clientes")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "viagens/painel/editar_cliente.html", {"form": form, "cliente": cliente})