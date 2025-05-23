from django import forms
from .models import SolicitacaoOrcamento, DocumentoViagem, Cliente, Viagem
from django_select2.forms import ModelSelect2MultipleWidget
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
        fields = ['arquivo']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'endereco', 'numero', 'complemento', 'bairro', 'cep', 'cidade', 'uf', 'celular', 'telefone', 'data_nascimento', 'email']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'uf': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2, 'placeholder': 'UF'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 0000-0000'}),
            # Para os demais campos:
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ViagemForm(forms.ModelForm):
    clientes = forms.ModelMultipleChoiceField(
        queryset=Cliente.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'id': 'id_clientes',
            'class': 'form-control',
            'style': 'width: 100%'
        }),
        required=True
    )

    class Meta:
        model = Viagem
        fields = '__all__'
        widgets = {
            'data_ida': forms.DateInput(attrs={'type': 'date'}),
            'data_volta': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aqui, atualize o queryset para todos os clientes
        self.fields['clientes'].queryset = Cliente.objects.all()
