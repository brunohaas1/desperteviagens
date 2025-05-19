#!/bin/bash

echo "🚀 Iniciando deploy do projeto Desperte Viagens..."

# 1. Entrar na pasta do projeto
cd /opt/desperteviagens || exit

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Fazer pull das últimas alterações do Git
echo "📥 Fazendo git pull..."
git pull

# 4. Limpar style.css antigo (opcional, evita cache travado)
echo "🧹 Limpando style.css antigo..."
rm -f staticfiles/css/style.css

# 5. Rodar collectstatic
echo "⚙️  Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# 6. Reiniciar Gunicorn (ajuste o nome se for outro serviço)
echo "🔄 Reiniciando Gunicorn..."
sudo systemctl restart desperteviagens

# 7. Reiniciar Nginx
echo "🔄 Reiniciando Nginx..."
sudo systemctl restart nginx

echo "✅ Deploy finalizado com sucesso!"
