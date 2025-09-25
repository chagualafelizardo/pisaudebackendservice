# Este backend, foi desenvolvido por Felizardo L. A. Chaguala para o PI-SAUDE
# Esta api, foi desenvolvido por Felizardo Chaguala, para auxiliar na digitacao eficientes dos dados da colheidos e organizado em ficheiros em formato excel.

# O direito de uso da APi esta com a Jhpiego em Mocambique, qualquer outra entidade deve ter permissao para o uso desta APi

# Entao como fazer esta tarefa
<!-- 
    Opções de Implementação
    1. Usando a API do DHIS2
    O DHIS2 possui uma API RESTful robusta que permite enviar dados programaticamente. 
-->

# Para ver os dados que foram carregados
http://197.249.4.129:8088/api/29/dataValueSets?dataSet=bJi2QH24rm5&orgUnit=QSxnM0virqc&period=202501

# Substitua no seu código: isto quando eu salvava e nao consegui ver os dados os CATEGORY_COMBO_ID erra =! ATTRIBUTE_COMBO_ID e a ideia erra colocar o mesmo codigo
CATEGORY_COMBO_ID = "HllvX50cXC0"  # Usando o mesmo ID para COC e AOC
ATTRIBUTE_COMBO_ID = "HllvX50cXC0"

# Aqui e o codigo para tirar todos os dataElement de um dataSet
http://197.249.4.129:8088/api/dataSets/bJi2QH24rm5.json?fields=id,name,dataSetElements[dataElement[id,name,categoryCombo[categoryOptionCombos[id,name]]]]

pip install xlrd>=2.0.1 // para leitura de ficheiros tipo .xls/xlsx

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