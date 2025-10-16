# Dockerfile
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando de execução
CMD ["python", "app.py", "--host=0.0.0.0"]
