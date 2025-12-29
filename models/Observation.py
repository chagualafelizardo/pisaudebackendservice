from . import db
from sqlalchemy import Enum
import enum
from datetime import datetime
import re

# Enum para syncStatus
class SyncStatusEnum(enum.Enum):
    NotSyncronized = "Not Syncronized"
    Syncronized = "Syncronized"
    Updated = "Updated"
    
class Observation(db.Model):
    __tablename__ = 'observation'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nid = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(500), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(1000), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    datainiciotarv = db.Column(db.DateTime, nullable=False)
    datalevantamento = db.Column(db.DateTime, nullable=False)
    dataproximolevantamento = db.Column(db.DateTime, nullable=False)
    dataconsulta = db.Column(db.DateTime, nullable=False)
    dataproximaconsulta = db.Column(db.DateTime, nullable=False)
    dataalocacao = db.Column(db.DateTime, nullable=False)
    dataenvio = db.Column(db.DateTime, nullable=False)
    smssendernumber = db.Column(db.String(100), nullable=False)
    smssuporternumber = db.Column(db.String(100), nullable=False)
    dataprimeiracv = db.Column(db.DateTime, nullable=True)
    valorprimeiracv = db.Column(db.Float, nullable=True)  # Alterado para Float
    dataultimacv = db.Column(db.DateTime, nullable=True)
    valorultimacv = db.Column(db.Float, nullable=True)    # Alterado para Float
    linhaterapeutica = db.Column(db.String(100), nullable=False)
    regime = db.Column(db.String(100), nullable=False)

    # Novo campo para flat status
    status = db.Column(db.String(100), nullable=False)
    
    # Campos de sincronização
    syncStatus = db.Column(Enum(SyncStatusEnum), nullable=False, default=SyncStatusEnum.NotSyncronized)
    syncStatusDate = db.Column(db.DateTime, nullable=True)
    
    # NOVO CAMPO: Status do SMS (apenas string)
    smsStatus = db.Column(db.String(50), nullable=True, default=None)

    # Chaves estrangeiras
    stateId = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    textmessageId = db.Column(db.Integer, db.ForeignKey('textmessage.id'), nullable=False)
    grouptypeId = db.Column(db.Integer, db.ForeignKey('grouptype.id'), nullable=False)
    groupId = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    createAt = db.Column(db.DateTime, default=db.func.now())
    updateAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relacionamentos
    state = db.relationship('State', backref='state_observations')
    textmessage = db.relationship('Textmessage', backref='textmessage_observations')
    grouptype = db.relationship('Grouptype', backref='grouptype_observations')
    group = db.relationship('Group', backref='group_observations')
    location = db.relationship('Location', backref='location_observations')
    user = db.relationship('User', backref='user_observations')

    def __repr__(self):
        return f'<Observation {self.id} nid={self.nid}>'
    
    # Método para converter dados do Excel
    @classmethod
    def from_excel_data(cls, data, user_id, state_id, group_id, grouptype_id, location_id, textmessage_id, grupo_pacientes=None):
        """Cria uma Observation a partir de dados do Excel"""
        obs = cls()
        
        # Campos obrigatórios básicos
        obs.nid = str(data.get('nid', data.get('NID', ''))).strip()
        obs.fullname = str(data.get('fullname', data.get('FullName', data.get('NomeCompleto', '')))).strip()
        obs.gender = str(data.get('gender', data.get('Gender', data.get('sexo', data.get('Sexo', ''))))).strip()
        obs.age = str(data.get('age', data.get('Age', data.get('idade_actual', data.get('Idade', ''))))).strip()
        obs.contact = str(data.get('contact', data.get('Contact', data.get('telefone', data.get('Telefone', data.get('contacto_paciente', '')))))).strip()
        obs.occupation = str(data.get('occupation', data.get('Occupation', data.get('Profissao', '')))).strip()
        
        # Converter campos de data - use data atual apenas se for campo obrigatório
        obs.datainiciotarv = cls._parse_datetime(data.get('datainiciotarv', ''), default_to_now=True)
        obs.datalevantamento = cls._parse_datetime(data.get('datalevantamento', ''), default_to_now=True)
        obs.dataproximolevantamento = cls._parse_datetime(data.get('dataproximolevantamento', ''), default_to_now=True)
        obs.dataconsulta = cls._parse_datetime(data.get('dataconsulta', ''), default_to_now=True)
        obs.dataproximaconsulta = cls._parse_datetime(data.get('dataproximaconsulta', ''), default_to_now=True)
        obs.dataalocacao = cls._parse_datetime(data.get('dataalocacao', ''), default_to_now=True)
        obs.dataenvio = cls._parse_datetime(data.get('dataenvio', ''), default_to_now=True)
        
        # Campos de carga viral - datas podem ser nulas
        dataprimeiracv = data.get('dataprimeiracv', data.get('data_primeira_carga', data.get('data_primeiro_carga', '')))
        obs.dataprimeiracv = cls._parse_datetime(dataprimeiracv, default_to_now=False)
        
        dataultimacv = data.get('dataultimacv', data.get('data_ultima_carga', data.get('data_ultimo_carga', '')))
        obs.dataultimacv = cls._parse_datetime(dataultimacv, default_to_now=False)
        
        # Converter campos float - IMPORTANTE: retornar None para valores vazios
        valorprimeiracv = data.get('valorprimeiracv', data.get('valor_primeira_carga', data.get('valor_primeiro_carga', '')))
        obs.valorprimeiracv = cls._parse_float(valorprimeiracv)
        
        valorultimacv = data.get('valorultimacv', data.get('valor_ultima_carga', data.get('valor_ultimo_carga', '')))
        obs.valorultimacv = cls._parse_float(valorultimacv)
        
        # Outros campos
        obs.linhaterapeutica = str(data.get('linhaterapeutica', '')).strip()
        obs.regime = str(data.get('regime', '')).strip()
        obs.status = 'Inicial'  # Default value
        obs.smssendernumber = str(data.get('smssendernumber', '')).strip()
        obs.smssuporternumber = str(data.get('smssuporternumber', '')).strip()
        
        # Se grupo_pacientes for fornecido, use como status
        if grupo_pacientes:
            obs.status = grupo_pacientes
        
        # IDs de relacionamento
        obs.userId = user_id
        obs.stateId = state_id
        obs.groupId = group_id
        obs.grouptypeId = grouptype_id
        obs.locationId = location_id
        obs.textmessageId = textmessage_id
        
        return obs
    
    @staticmethod
    def _parse_datetime(value, default_to_now=True):
        """Converte string para datetime. Retorna None se vazio e default_to_now=False."""
        if not value or str(value).strip() == '':
            return datetime.now() if default_to_now else None
            
        try:
            # Tenta converter de string para datetime
            if isinstance(value, str):
                # Remove espaços extras
                value = value.strip()
                
                # Se estiver vazio após strip
                if value == '':
                    return datetime.now() if default_to_now else None
                
                # Remover "T00:00:00" ou "T00:00" do final
                if 'T00:00:00' in value:
                    value = value.replace('T00:00:00', '')
                elif 'T00:00' in value:
                    value = value.replace('T00:00', '')
                
                # Tenta vários formatos de data
                date_formats = [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d',
                    '%d/%m/%Y %H:%M:%S',
                    '%d/%m/%Y',
                    '%m/%d/%Y %H:%M:%S',
                    '%m/%d/%Y',
                    '%d-%m-%Y',
                    '%m-%d-%Y'
                ]
                
                for fmt in date_formats:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
                
                # Se nenhum formato funcionar, retorna data atual ou None
                return datetime.now() if default_to_now else None
            elif isinstance(value, (int, float)):
                # Se for número (timestamp do Excel)
                return datetime.fromtimestamp(value)
            else:
                return datetime.now() if default_to_now else None
        except Exception as e:
            print(f"Error parsing datetime '{value}': {e}")
            return datetime.now() if default_to_now else None
    
    @staticmethod
    def _parse_float(value):
        """Converte string para float. Retorna None se vazio."""
        if value is None or value == '' or str(value).strip() == '':
            return None
            
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                # Remove espaços
                cleaned = value.strip()
                
                # Se estiver vazio após limpeza
                if cleaned == '' or cleaned.lower() == 'null' or cleaned.lower() == 'none':
                    return None
                
                # Converte vírgula para ponto
                cleaned = cleaned.replace(',', '.')
                
                # Remove caracteres não numéricos exceto ponto, sinal negativo e 'e' para notação científica
                cleaned = re.sub(r'[^\d\.\-eE]', '', cleaned)
                
                # Se estiver vazio após limpeza
                if cleaned == '':
                    return None
                
                return float(cleaned)
            else:
                return None
        except Exception as e:
            print(f"Error converting to float: '{value}', error: {e}")
            return None
    
    @staticmethod
    def _parse_int(value):
        """Converte string para inteiro (mantido para outros campos)"""
        if not value or str(value).strip() == '':
            return 0
            
        try:
            if isinstance(value, (int, float)):
                return int(value)
            elif isinstance(value, str):
                # Remove caracteres não numéricos
                cleaned = ''.join(filter(str.isdigit, value))
                return int(cleaned) if cleaned else 0
            else:
                return 0
        except Exception:
            return 0