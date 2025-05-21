from django import forms
from .models import SolicitacaoOrcamento , DocumentoViagem , Cliente , Viagem

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
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'email', 'telefone', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        exclude = ['cliente']
        widgets = {
            'data_ida': forms.DateInput(attrs={'type': 'date'}),
            'data_volta': forms.DateInput(attrs={'type': 'date'}),
        } 
class DocumentoViagemForm(forms.ModelForm):
    class Meta:
        model = DocumentoViagem
        fields = ['arquivo']       