# Este backend, foi desenvolvido por Felizardo L. A. Chaguala para o PI-SAUDE
pip install flask
python -m pip install flask
python3 -m pip install flask
pip install flask_sqlalchemy
python -m pip install flask_sqlalchemy
pip install -r requirements.txt
pip install psycopg2-binary
python app.py

# Re-estruturacao das tabelas
id: autoincrement
nid:
fullname:
gender:
age:
datainiciotarv:
datalevantamento:
dataproximolevantamento:
dataconsulta:
dataproximaconsulta:
contact:
occupation:
dataalocacao:
dataenvio:
dataretorno:
smssendernumber:
smssuporternumber:
grupotypeid:
grupoid:
locationid:
dataprimeiracv:
valorprimeiracv:
dataultimacv:
valorultimacv:
linhaterapeutica:
regime:
estado:
textmessageid:

textmessage:
    - id:
    - messagetext:

estadoid:
    - id
    - descriton:


userid:
    - id:
    - fullname:
    - username:
    - password:
    - email:
    - profil:
    - contact:
    - roleid:
    - locationid

role:
    - id:
    - description:

location:
    - id:
    - name
    - descrition
    - location
    - locationLat
    - locationLng

grupotypeid:
    - id:
    - description:

grupo:
    - id
    - description:

# Depois mudar o servidor para um mais profissional
AVISO: Este é um servidor de desenvolvimento. Não o utilize numa implantação de produção. Em vez disso, utilize um servidor WSGI de produção.