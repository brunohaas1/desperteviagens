from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Viagem
from django.db.models import Count

@staff_member_required
def relatorio_viagens(request):
    # Contar viagens por status
    viagens_status = Viagem.objects.values('status').annotate(total=Count('id'))

    # Separar dados para o gráfico
    labels = []
    data = []

    for item in viagens_status:
        labels.append(dict(Viagem.STATUS_CHOICES).get(item['status'], item['status']))
        data.append(item['total'])

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'admin/relatorios_viagens.html', context)
