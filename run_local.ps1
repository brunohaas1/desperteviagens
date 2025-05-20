# Script para rodar o Django localmente com ENV=LOCAL
Write-Host "Iniciando o servidor Django em ambiente LOCAL..."

# Define a variável de ambiente
$env:ENV = "LOCAL"

# Roda o servidor de desenvolvimento
python manage.py runserver
