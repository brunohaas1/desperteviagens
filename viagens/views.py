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