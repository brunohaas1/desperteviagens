from django import forms
from .models import SolicitacaoOrcamento

class SolicitacaoOrcamentoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoOrcamento
        fields = ['nome', 'sobrenome', 'email', 'telefone', 'destino', 'data_viagem']
