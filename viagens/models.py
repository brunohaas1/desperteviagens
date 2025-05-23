from django.db import models
from datetime import timedelta
import os

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
    email = models.EmailField(blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)  # Formato CPF com máscara opcional
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)  # Formato CEP
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)  # Sigla do estado
    celular = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.nome

class Viagem(models.Model):
    STATUS_CHOICES = [
        ('andamento', 'Em andamento'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    clientes = models.ManyToManyField(Cliente)
    destino = models.CharField(max_length=150)
    data_ida = models.DateField()
    data_volta = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='andamento')
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True)  # Novo campo automático

    def __str__(self):
        nomes = ", ".join([c.nome for c in self.clientes.all()])
        return f"{self.destino} - {nomes}"

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
    viagem = models.ForeignKey('Viagem', on_delete=models.CASCADE, related_name="documentos_viagem")
    arquivo = models.FileField(upload_to='documentos_viagem/')

    def delete(self, *args, **kwargs):
        # Deleta o arquivo físico
        if self.arquivo and os.path.isfile(self.arquivo.path):
            os.remove(self.arquivo.path)
        # Depois remove do banco
        super().delete(*args, **kwargs)
