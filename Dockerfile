FROM python:3.11-slim

# Evita criação de ficheiros .pyc e melhora logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (útil para alguns pacotes)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia primeiro o requirements.txt (melhora cache)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip && \
    pip uninstall -y Flask-Babel || true && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir Babel==2.14.0

# Copia arquivos de configuração
COPY babel.cfg .
COPY init_translations.py .
COPY docker-entrypoint.sh .

# Dá permissão de execução ao entrypoint
RUN chmod +x docker-entrypoint.sh

# Copia todo o código do projeto
COPY . .

# Cria diretório para traduções
RUN mkdir -p translations

# Expõe a porta padrão do Flask
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Use o entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]