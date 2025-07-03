# Quando pretendo configurar DATABASE_URL na varial de ambiante do sistema
# class Config:
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# Quando estou fazer o acesso a Db usando o path URL

import os

class Config:
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/pisaude'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração da porta
    PORT = 5000
    DEBUG = True
