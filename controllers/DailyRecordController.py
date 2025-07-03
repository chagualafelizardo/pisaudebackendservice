from flask import jsonify, request
from models import db, DailyRecord
from datetime import datetime

class DailyRecordController:
    @staticmethod
    def get_all():
        try:
            records = DailyRecord.query.all()
            return jsonify([{
                'id': r.id,
                'datasistema': r.datasistema,
                'dataregisto': r.dataregisto,
                'idade': r.idade,
                'idadeunidade': r.idadeunidade,
                'sexo': r.sexo,
                'parceirosexual': r.parceirosexual,
                'filhomenordezanos': r.filhomenordezanos,
                'maepaiCIPeddezanos': r.maepaiCIPeddezanos,
                'confirmacaoautoteste_hiv': r.confirmacaoautoteste_hiv,
                'testagemdetermine1': r.testagemdetermine1,
                'testagemunigold1': r.testagemunigold1,
                'testagemdetermine2': r.testagemdetermine2,
                'testagemunigold2': r.testagemunigold2,
                'resultadofinal': r.resultadofinal,
                'historialtestagem_primeira_testado': r.historialtestagem_primeira_testado,
                'historialtestagem_positivo_no_passado': r.historialtestagem_positivo_no_passado,
                'ocupacao': r.ocupacao,
                'referenciaconselheironome': r.referenciaconselheironome,
                'cpnopcao': r.cpnopcao,
                'casoindiceopcao': r.casoindiceopcao,
                'cpfopcao': r.cpfopcao,
                'latitude': r.latitude,
                'longitude': r.longitude,
                'sincronizado': r.sincronizado,
                'ultima_sincronizacao': r.ultima_sincronizacao,
                'locationId': r.locationId,
                'portatestagemId': r.portatestagemId,
                'referenciauserId': r.referenciauserId,
                'populacaochaveId': r.populacaochaveId,
                'ligacaocontactosId': r.ligacaocontactosId,
                'registocontactoId': r.registocontactoId,
                'userId': r.userId,
                'createAt': r.createAt,
                'updateAt': r.updateAt
            } for r in records]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            record = DailyRecord.query.get(id)
            if record:
                return jsonify({
                    'id': record.id,
                    'datasistema': record.datasistema,
                    'dataregisto': record.dataregisto,
                    'idade': record.idade,
                    'idadeunidade': record.idadeunidade,
                    'sexo': record.sexo,
                    'parceirosexual': record.parceirosexual,
                    'filhomenordezanos': record.filhomenordezanos,
                    'maepaiCIPeddezanos': record.maepaiCIPeddezanos,
                    'confirmacaoautoteste_hiv': record.confirmacaoautoteste_hiv,
                    'testagemdetermine1': record.testagemdetermine1,
                    'testagemunigold1': record.testagemunigold1,
                    'testagemdetermine2': record.testagemdetermine2,
                    'testagemunigold2': record.testagemunigold2,
                    'resultadofinal': record.resultadofinal,
                    'historialtestagem_primeira_testado': record.historialtestagem_primeira_testado,
                    'historialtestagem_positivo_no_passado': record.historialtestagem_positivo_no_passado,
                    'ocupacao': record.ocupacao,
                    'referenciaconselheironome': record.referenciaconselheironome,
                    'cpnopcao': record.cpnopcao,
                    'casoindiceopcao': record.casoindiceopcao,
                    'cpfopcao': record.cpfopcao,
                    'latitude': record.latitude,
                    'longitude': record.longitude,
                    'sincronizado': record.sincronizado,
                    'ultima_sincronizacao': record.ultima_sincronizacao,
                    'locationId': record.locationId,
                    'portatestagemId': record.portatestagemId,
                    'referenciauserId': record.referenciauserId,
                    'populacaochaveId': record.populacaochaveId,
                    'ligacaocontactosId': record.ligacaocontactosId,
                    'registocontactoId': record.registocontactoId,
                    'userId': record.userId,
                    'createAt': record.createAt,
                    'updateAt': record.updateAt
                }), 200
            return jsonify({'message': 'Daily record not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            novo_record = DailyRecord(
                datasistema=datetime.strptime(data['datasistema'], '%Y-%m-%dT%H:%M:%S'),
                dataregisto=datetime.strptime(data['dataregisto'], '%Y-%m-%dT%H:%M:%S'),
                idade=data['idade'],
                idadeunidade=data['idadeunidade'],
                sexo=data['sexo'],
                parceirosexual=data['parceirosexual'],
                filhomenordezanos=data['filhomenordezanos'],
                maepaiCIPeddezanos=data['maepaiCIPeddezanos'],
                confirmacaoautoteste_hiv=data['confirmacaoautoteste_hiv'],
                testagemdetermine1=data['testagemdetermine1'],
                testagemunigold1=data['testagemunigold1'],
                testagemdetermine2=data['testagemdetermine2'],
                testagemunigold2=data['testagemunigold2'],
                resultadofinal=data['resultadofinal'],
                historialtestagem_primeira_testado=data['historialtestagem_primeira_testado'],
                historialtestagem_positivo_no_passado=data['historialtestagem_positivo_no_passado'],
                ocupacao=data['ocupacao'],
                referenciaconselheironome=data['referenciaconselheironome'],
                cpnopcao=data['cpnopcao'],
                casoindiceopcao=data['casoindiceopcao'],
                cpfopcao=data['cpfopcao'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                sincronizado=data['sincronizado'],
                ultima_sincronizacao=data['ultima_sincronizacao'],
                locationId=data['locationId'],
                portatestagemId=data['portatestagemId'],
                referenciauserId=data['referenciauserId'],
                populacaochaveId=data['populacaochaveId'],
                ligacaocontactosId=data['ligacaocontactosId'],
                registocontactoId=data['registocontactoId'],
                userId=data['userId']
            )
            db.session.add(novo_record)
            db.session.commit()
            return jsonify({'message': 'Daily record created', 'id': novo_record.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            record = DailyRecord.query.get(id)
            if not record:
                return jsonify({'message': 'Daily record not found'}), 404

            db.session.delete(record)
            db.session.commit()

            return jsonify({'message': 'Daily record deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
