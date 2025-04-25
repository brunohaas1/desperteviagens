from django.db import models



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
