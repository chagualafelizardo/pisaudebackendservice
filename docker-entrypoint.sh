#!/bin/bash
# docker-entrypoint.sh

set -e

echo "🚀 Iniciando aplicação PI-SAÚDE..."

# Verifica e inicializa traduções se necessário
if [ ! -f "translations/pt/LC_MESSAGES/messages.mo" ]; then
    echo "📚 Arquivos de tradução não encontrados. Inicializando..."
    python init_translations.py
else
    echo "✅ Traduções já inicializadas."
fi

# Atualiza traduções se houver mudanças (opcional)
if [ "$UPDATE_TRANSLATIONS" = "true" ]; then
    echo "🔄 Atualizando traduções..."
    pybabel update -i messages.pot -d translations
    pybabel compile -d translations
fi

# Executa as migrações do banco de dados (se usar Flask-Migrate)
if command -v flask &> /dev/null; then
    echo "🗄️  Verificando migrações do banco de dados..."
    flask db upgrade || echo "⚠️  Aviso: Não foi possível atualizar banco de dados"
fi

# Inicia a aplicação Flask
echo "🌐 Iniciando servidor Flask..."
exec flask run --host=0.0.0.0 --reload