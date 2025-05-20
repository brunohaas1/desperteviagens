from django.shortcuts import render, get_object_or_404, redirect
from .models import  SolicitacaoOrcamento
from .forms import SolicitacaoOrcamentoForm
from django.core.mail import send_mail


from django.shortcuts import render

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