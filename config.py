import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1/pisaude'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = 5000
    DEBUG = True