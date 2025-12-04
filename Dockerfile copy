FROM python:3.11-slim

# Evita criação de ficheiros .pyc e melhora logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define diretório de trabalho
WORKDIR /app

# Copia primeiro o requirements.txt (melhora cache)
COPY requirements.txt .

# Instala dependências e corrige conflito com Flask-Babel
RUN pip install --upgrade pip && \
    pip uninstall -y Flask-Babel || true && \
    pip install --no-cache-dir Flask==2.3.3 Flask-BabelEx==0.9.4 Flask-CORS==4.0.0 && \
    pip install --no-cache-dir numpy==1.26.4 && \
    pip install --no-cache-dir -r requirements.txt


# Copia todo o código do projeto
COPY . .

# Expõe a porta padrão do Flask
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# 🔥 Comando final com reload automático
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
