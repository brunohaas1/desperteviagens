from django.shortcuts import render, redirect ,get_object_or_404
from .forms import SolicitacaoOrcamentoForm
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from .models import Cliente, Viagem, DocumentoViagem 
from django.views.decorators.http import require_POST
from .forms import ClienteForm , ViagemForm ,DocumentoViagemForm
from django.db.models import Q
from django.utils.timezone import now
from django.db.models import Sum
from datetime import timedelta
import openpyxl
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pandas as pd
from django.http import JsonResponse
from django.utils.text import slugify
from django.template.loader import get_template
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm 
from reportlab.lib import colors
from django.http import FileResponse
import os
from io import BytesIO
from django.conf import settings
from reportlab.lib.utils import ImageReader
from xhtml2pdf import pisa
from pathlib import Path

def home(request):
    return render(request, 'viagens/html/home.html')

def cotacao(request):
    if request.method == 'POST':
        form = SolicitacaoOrcamentoForm(request.POST)
        if form.is_valid():
            orcamento = form.save()

            # Envia o e-mail
            assunto = 'Nova solicitação de orçamento'
            mensagem = f"""
📩 Nova solicitação de orçamento:

Nome: {orcamento.nome} {orcamento.sobrenome}
Email: {orcamento.email}
Telefone: {orcamento.telefone}
Destino: {orcamento.destino}
Data da viagem: {orcamento.data_viagem.strftime('%d/%m/%Y')}
            """
            destinatarios = ['desperteviagens@gmail.com']  # Pode ser mais de um

            send_mail(assunto, mensagem, None, destinatarios)

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
def produtos(request):
    return render(request, 'viagens/html/produtos.html')



@staff_member_required
def dashboard_admin(request):
    hoje = now()
    mes_atual = hoje.month
    ano_atual = hoje.year

    faturamento_mes = Viagem.objects.filter(
        data_ida__month=mes_atual,
        data_ida__year=ano_atual
    ).aggregate(total=Sum("valor"))["total"] or 0

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

    return render(request, "viagens/painel/clientes.html", {
        "clientes": clientes,
        "busca": busca,
    })
def lista_viagens(request):
    status = request.GET.get("status")
    cliente_nome = request.GET.get("cliente_nome")

    viagens = Viagem.objects.all()

    if status:
        viagens = viagens.filter(status=status)

    if cliente_nome:
        viagens = viagens.filter(cliente__nome__icontains=cliente_nome)

    clientes = Cliente.objects.all()

    return render(request, "viagens/painel/viagens.html", {
        "viagens": viagens,
        "clientes": clientes,
        "status_ativo": status,
        "cliente_ativo": cliente_nome
    })
def lista_documentos(request):
    documentos = DocumentoViagem.objects.select_related("viagem", "viagem__cliente").all().order_by("-id")
    return render(request, "viagens/painel/documentos.html", {"documentos": documentos})
@require_POST
def delete_documento(request, doc_id):
    documento = get_object_or_404(DocumentoViagem, id=doc_id)
    documento.delete()
    return redirect("painel:lista_viagens")
def adicionar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("painel:lista_clientes")
    else:
        form = ClienteForm()
    return render(request, "viagens/painel/adicionar_cliente.html", {"form": form})


def adicionar_viagem(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    if request.method == "POST":
        form = ViagemForm(request.POST)
        if form.is_valid():
            viagem = form.save(commit=False)
            viagem.cliente = cliente
            viagem.save()
            return redirect("painel:lista_clientes")
    else:
        form = ViagemForm()
    return render(request, "viagens/painel/adicionar_viagem.html", {"form": form, "cliente": cliente})
def adicionar_documento(request, viagem_id):
    viagem = Viagem.objects.get(id=viagem_id)
    if request.method == "POST":
        form = DocumentoViagemForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.viagem = viagem
            doc.save()
            return redirect("painel:lista_viagens")
    else:
        form = DocumentoViagemForm()
    return render(request, "viagens/painel/adicionar_documento.html", {
        "form": form,
        "viagem": viagem
    })

def exportar_viagens_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Viagens"

    ws.append(['Cliente', 'Destino', 'Data Ida', 'Data Volta', 'Valor', 'Status'])

    for viagem in Viagem.objects.select_related('cliente').all():
        ws.append([
            viagem.cliente.nome,
            viagem.destino,
            viagem.data_ida.strftime('%d/%m/%Y'),
            viagem.data_volta.strftime('%d/%m/%Y'),
            f"{viagem.valor:.2f}",
            viagem.status
        ])

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

    viagens = Viagem.objects.select_related('cliente').all()

    p.drawString(40, y, "Cliente")
    p.drawString(150, y, "Destino")
    p.drawString(250, y, "Ida")
    p.drawString(300, y, "Volta")
    p.drawString(370, y, "Valor")
    p.drawString(430, y, "Status")

    y -= 20

    for v in viagens:
        if y < 60:  # Nova página se estiver muito abaixo
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 50

        p.drawString(40, y, v.cliente.nome[:20])
        p.drawString(150, y, v.destino[:15])
        p.drawString(250, y, v.data_ida.strftime('%d/%m/%Y'))
        p.drawString(300, y, v.data_volta.strftime('%d/%m/%Y'))
        p.drawString(370, y, f"R$ {v.valor:.2f}")
        p.drawString(430, y, v.status)

        y -= 20

    p.showPage()
    p.save()
    return response

def exportar_clientes_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_clientes.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Relatório de Clientes")

    p.setFont("Helvetica", 10)
    y = height - 100

    p.drawString(40, y, "Nome")
    p.drawString(200, y, "CPF")
    p.drawString(300, y, "E-mail")
    p.drawString(430, y, "Telefone")

    y -= 20

    for cliente in Cliente.objects.all():
        if y < 60:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = height - 50

        p.drawString(40, y, cliente.nome[:25])
        p.drawString(200, y, cliente.cpf or "-")
        p.drawString(300, y, cliente.email[:20] or "-")
        p.drawString(430, y, cliente.telefone or "-")
        y -= 20

    p.showPage()
    p.save()
    return response


def exportar_clientes_excel(request):
    clientes = Cliente.objects.all().values("nome", "cpf", "email", "telefone", "data_nascimento")
    df = pd.DataFrame(clientes)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=relatorio_clientes.xlsx'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Clientes')
    
    return response

@staff_member_required
def agenda_viagens(request):
    return render(request, "viagens/painel/agenda.html")



def eventos_viagens(request):
    eventos = []
    for viagem in Viagem.objects.all():
        eventos.append({
            "title": f"{viagem.cliente.nome} - {viagem.destino}",
            "start": viagem.data_ida.isoformat(),
            "end": viagem.data_volta.isoformat(),
        })
    return JsonResponse(eventos, safe=False)

def link_callback(uri, rel):
    """
    Retorna o caminho físico correto para imagens locais.
    """
    result = os.path.join(settings.BASE_DIR, uri.replace(settings.STATIC_URL, "static/"))
    return result
def gerar_contrato_pdf(request, viagem_id):
    viagem = Viagem.objects.get(id=viagem_id)

    template = get_template("viagens/painel/contrato.html")
    html = template.render({
        "viagem": viagem,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="contrato.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse("Erro ao gerar PDF", status=500)

    return response