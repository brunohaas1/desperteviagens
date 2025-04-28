from django.db import models
from datetime import timedelta


class SolicitacaoOrcamento(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    destino = models.CharField(max_length=100)
    data_viagem = models.DateField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.destino}"
class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True)  # Novo campo automático

    def __str__(self):
        return self.nome

class Viagem(models.Model):
    STATUS_CHOICES = [
        ('andamento', 'Em andamento'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='viagens')
    destino = models.CharField(max_length=150)
    data_ida = models.DateField()
    data_volta = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='andamento')
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True)  # Novo campo automático

    def __str__(self):
        return f"{self.destino} - {self.cliente.nome}"

    @property
    def duracao_viagem(self):
        return (self.data_volta - self.data_ida).days

    @property
    def valor_por_dia(self):
        dias = self.duracao_viagem
        if dias > 0:
            return self.valor / dias
        return 0


class DocumentoViagem(models.Model):
    viagem = models.ForeignKey('Viagem', on_delete=models.CASCADE, related_name='documentos_viagem')
    arquivo = models.FileField(upload_to='documentos_viagem/')

    def __str__(self):
        return f"Documento ({self.viagem.destino})"
    