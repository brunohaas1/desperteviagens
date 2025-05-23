# Generated by Django 5.2 on 2025-05-23 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cpf', models.CharField(blank=True, max_length=14, null=True)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('numero', models.CharField(blank=True, max_length=10, null=True)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('cep', models.CharField(blank=True, max_length=9, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('uf', models.CharField(blank=True, max_length=2, null=True)),
                ('celular', models.CharField(blank=True, max_length=20, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitacaoOrcamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('destino', models.CharField(max_length=100)),
                ('data_viagem', models.DateField()),
                ('data_solicitacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Viagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destino', models.CharField(max_length=150)),
                ('data_ida', models.DateField()),
                ('data_volta', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('andamento', 'Em andamento'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')], default='andamento', max_length=20)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
                ('clientes', models.ManyToManyField(to='viagens.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoViagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='documentos_viagem/')),
                ('viagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos_viagem', to='viagens.viagem')),
            ],
        ),
    ]
