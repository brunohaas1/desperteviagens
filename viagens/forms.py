from django import forms
from .models import SolicitacaoOrcamento , DocumentoViagem

class SolicitacaoOrcamentoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoOrcamento
        fields = ['nome', 'sobrenome', 'email', 'telefone', 'destino', 'data_viagem']

        widgets = {
            'telefone': forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'id_telefone',
            'placeholder': '(00) 00000-0000',
            'autocomplete': 'off',
}),

            
            'data_viagem': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_data_viagem',
                'autocomplete': 'off',
                'placeholder': 'Selecione a data'
}),


}
class DocumentoViagemForm(forms.ModelForm):
    class Meta:
        model = DocumentoViagem
        fields = ('arquivo',)
