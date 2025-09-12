from flask import jsonify, request
from datetime import datetime
from models import db, Observation, State, Textmessage, Grouptype, Group, Location, User

class ObservationController:
    @staticmethod
    def get_all():
        try:
            observations = Observation.query.all()
            return jsonify([{
                'id': obs.id,
                'nid': obs.nid,
                'fullname': obs.fullname,
                'gender': obs.gender,
                'age': obs.age,
                'contact': obs.contact,
                'occupation': obs.occupation,
                'datainiciotarv': obs.datainiciotarv.isoformat(),
                'datalevantamento': obs.datalevantamento.isoformat(),
                'dataproximolevantamento': obs.dataproximolevantamento.isoformat(),
                'dataconsulta': obs.dataconsulta.isoformat(),
                'dataproximaconsulta': obs.dataproximaconsulta.isoformat(),
                'dataalocacao': obs.dataalocacao.isoformat(),
                'dataenvio': obs.dataenvio.isoformat(),
                'smssendernumber': obs.smssendernumber,
                'smssuporternumber': obs.smssuporternumber,
                'dataprimeiracv': obs.dataprimeiracv.isoformat(),
                'valorprimeiracv': obs.valorprimeiracv,
                'dataultimacv': obs.dataultimacv.isoformat(),
                'valorultimacv': obs.valorultimacv,
                'linhaterapeutica': obs.linhaterapeutica,
                'regime': obs.regime,
                'stateId': obs.stateId,
                'textmessageId': obs.textmessageId,
                'grouptypeId': obs.grouptypeId,
                'groupId': obs.groupId,
                'locationId': obs.locationId,
                'userId': obs.userId,
                'createAt': obs.createAt.isoformat(),
                'updateAt': obs.updateAt.isoformat(),
                'state': {'id': obs.state.id, 'description': obs.state.description} if obs.state else None,
                'textmessage': {'id': obs.textmessage.id, 'messagetext': obs.textmessage.messagetext} if obs.textmessage else None,
                'grouptype': {'id': obs.grouptype.id, 'description': obs.grouptype.description} if obs.grouptype else None,
                'group': {'id': obs.group.id, 'description': obs.group.description} if obs.group else None,
                'location': {'id': obs.location.id, 'name': obs.location.name} if obs.location else None,
                'user': {'id': obs.user.id, 'fullname': obs.user.fullname} if obs.user else None
            } for obs in observations]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            observation = Observation.query.get(id)
            if observation:
                return jsonify({
                    'id': observation.id,
                    'nid': observation.nid,
                    'fullname': observation.fullname,
                    'gender': observation.gender,
                    'age': observation.age,
                    'contact': observation.contact,
                    'occupation': observation.occupation,
                    'datainiciotarv': observation.datainiciotarv.isoformat(),
                    'datalevantamento': observation.datalevantamento.isoformat(),
                    'dataproximolevantamento': observation.dataproximolevantamento.isoformat(),
                    'dataconsulta': observation.dataconsulta.isoformat(),
                    'dataproximaconsulta': observation.dataproximaconsulta.isoformat(),
                    'dataalocacao': observation.dataalocacao.isoformat(),
                    'dataenvio': observation.dataenvio.isoformat(),
                    'smssendernumber': observation.smssendernumber,
                    'smssuporternumber': observation.smssuporternumber,
                    'dataprimeiracv': observation.dataprimeiracv.isoformat(),
                    'valorprimeiracv': observation.valorprimeiracv,
                    'dataultimacv': observation.dataultimacv.isoformat(),
                    'valorultimacv': observation.valorultimacv,
                    'linhaterapeutica': observation.linhaterapeutica,
                    'regime': observation.regime,
                    'stateId': observation.stateId,
                    'textmessageId': observation.textmessageId,
                    'grouptypeId': observation.grouptypeId,
                    'groupId': observation.groupId,
                    'locationId': observation.locationId,
                    'userId': observation.userId,
                    'createAt': observation.createAt.isoformat(),
                    'updateAt': observation.updateAt.isoformat(),
                    'state': {'id': observation.state.id, 'description': observation.state.description} if observation.state else None,
                    'textmessage': {'id': observation.textmessage.id, 'messagetext': observation.textmessage.messagetext} if observation.textmessage else None,
                    'grouptype': {'id': observation.grouptype.id, 'description': observation.grouptype.description} if observation.grouptype else None,
                    'group': {'id': observation.group.id, 'description': observation.group.description} if observation.group else None,
                    'location': {'id': observation.location.id, 'name': observation.location.name} if observation.location else None,
                    'user': {'id': observation.user.id, 'fullname': observation.user.fullname} if observation.user else None
                }), 200
            return jsonify({'message': 'Observation not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            
            # Validação dos campos obrigatórios
            required_fields = ['nid', 'fullname', 'gender', 'age', 'contact', 'occupation',
                             'datainiciotarv', 'datalevantamento', 'dataproximolevantamento',
                             'dataconsulta', 'dataproximaconsulta', 'dataalocacao', 'dataenvio',
                             'smssendernumber', 'smssuporternumber', 'dataprimeiracv', 'valorprimeiracv',
                             'dataultimacv', 'valorultimacv', 'linhaterapeutica', 'regime',
                             'stateId', 'textmessageId', 'grouptypeId', 'groupId', 'locationId', 'userId']
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

            # Verifica se as FKs existem
            related_models = {
                'stateId': State,
                'textmessageId': Textmessage,
                'grouptypeId': Grouptype,
                'groupId': Group,
                'locationId': Location,
                'userId': User
            }

            for field, model in related_models.items():
                if not model.query.get(data[field]):
                    return jsonify({'message': f'{model.__name__} with id {data[field]} not found'}), 404

            # Cria nova observação
            new_observation = Observation(
                nid=data['nid'],
                fullname=data['fullname'],
                gender=data['gender'],
                age=data['age'],
                contact=data['contact'],
                occupation=data['occupation'],
                datainiciotarv=datetime.fromisoformat(data['datainiciotarv']),
                datalevantamento=datetime.fromisoformat(data['datalevantamento']),
                dataproximolevantamento=datetime.fromisoformat(data['dataproximolevantamento']),
                dataconsulta=datetime.fromisoformat(data['dataconsulta']),
                dataproximaconsulta=datetime.fromisoformat(data['dataproximaconsulta']),
                dataalocacao=datetime.fromisoformat(data['dataalocacao']),
                dataenvio=datetime.fromisoformat(data['dataenvio']),
                smssendernumber=data['smssendernumber'],
                smssuporternumber=data['smssuporternumber'],
                dataprimeiracv=datetime.fromisoformat(data['dataprimeiracv']),
                valorprimeiracv=data['valorprimeiracv'],
                dataultimacv=datetime.fromisoformat(data['dataultimacv']),
                valorultimacv=data['valorultimacv'],
                linhaterapeutica=data['linhaterapeutica'],
                regime=data['regime'],
                stateId=data['stateId'],
                textmessageId=data['textmessageId'],
                grouptypeId=data['grouptypeId'],
                groupId=data['groupId'],
                locationId=data['locationId'],
                userId=data['userId']
            )

            db.session.add(new_observation)
            db.session.commit()

            return jsonify({
                'id': new_observation.id,
                'message': 'Observation created successfully'
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400

            # Atualiza campos simples
            simple_fields = ['fullname', 'gender', 'age', 'contact', 'occupation',
                           'smssendernumber', 'smssuporternumber', 'linhaterapeutica', 'regime']
            
            for field in simple_fields:
                if field in data:
                    setattr(observation, field, data[field])

            # Atualiza campos de data
            date_fields = ['datainiciotarv', 'datalevantamento', 'dataproximolevantamento',
                         'dataconsulta', 'dataproximaconsulta', 'dataalocacao', 'dataenvio',
                         'dataprimeiracv', 'dataultimacv']
            
            for field in date_fields:
                if field in data:
                    setattr(observation, field, datetime.fromisoformat(data[field]))

            # Atualiza campos numéricos
            if 'valorprimeiracv' in data:
                observation.valorprimeiracv = data['valorprimeiracv']
            if 'valorultimacv' in data:
                observation.valorultimacv = data['valorultimacv']

            # Atualiza relacionamentos
            related_models = {
                'stateId': State,
                'textmessageId': Textmessage,
                'grouptypeId': Grupotype,
                'groupId': Grupo,
                'locationId': Location,
                'userId': User
            }

            for field, model in related_models.items():
                if field in data:
                    if not model.query.get(data[field]):
                        return jsonify({'message': f'{model.__name__} with id {data[field]} not found'}), 404
                    setattr(observation, field, data[field])

            observation.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Observation updated successfully',
                'id': observation.id
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            db.session.delete(observation)
            db.session.commit()

            return jsonify({'message': 'Observation deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500