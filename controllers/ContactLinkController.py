from flask import jsonify, request
from models import db
from models.ContactLink import ContactLink
from datetime import datetime

class ContactLinkController:
    @staticmethod
    def get_all():
        try:
            contact_links = ContactLink.query.all()
            result = []
            for link in contact_links:
                result.append({
                    'id': link.id,
                    'data_sistema': link.data_sistema,
                    'data_registo': link.data_registo,
                    'nomeutente': link.nomeutente,
                    'endereco': link.endereco,
                    'telefone': link.telefone,
                    'nestaus': link.nestaus,
                    'outraus': link.outraus,
                    'nameustarv': link.nameustarv,
                    'nid': link.nid,
                    'dataprimeiraconsultaclinica': link.dataprimeiraconsultaclinica,
                    'ligacaoconfirmada': link.ligacaoconfirmada,
                    'parceirosexual': link.parceirosexual,
                    'parceirosexualquantos': link.parceirosexualquantos,
                    'filhomenordezanos': link.filhomenordezanos,
                    'filhomenordezanosquantos': link.filhomenordezanosquantos,
                    'maepaiCIPeddezanos': link.maepaiCIPeddezanos,
                    'maepaiCIPeddezanosquantos': link.maepaiCIPeddezanosquantos,
                    'ocupacao': link.ocupacao,
                    'obs': link.obs,
                    'referenciaconselheironome': link.referenciaconselheironome,
                    'sincronizado': link.sincronizado,
                    'ultimasincronizacao': link.ultimasincronizacao,
                    'locationId': link.locationId,
                    'location': link.location.name if link.location else None,
                    'portatestagemId': link.portatestagemId,
                    'portatestagem': link.portatestagem.nome if link.portatestagem else None,
                    'referenciauserId': link.referenciauserId,
                    'referenciauser': link.referenciauser.username if link.referenciauser else None,
                    'userId': link.userId,
                    'user': link.user.username if link.user else None,
                    'keypopulationId': link.keypopulationId,
                    'keypopulation': link.keypopulation.description if link.keypopulation else None,
                    'ligacaocontactosId': link.ligacaocontactosId,
                    'registocontactoId': link.registocontactoId,
                    'createAt': link.createAt,
                    'updateAt': link.updateAt
                })
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            link = ContactLink.query.get(id)
            if link:
                result = {
                    'id': link.id,
                    'data_sistema': link.data_sistema,
                    'data_registo': link.data_registo,
                    'nomeutente': link.nomeutente,
                    'endereco': link.endereco,
                    'telefone': link.telefone,
                    'nestaus': link.nestaus,
                    'outraus': link.outraus,
                    'nameustarv': link.nameustarv,
                    'nid': link.nid,
                    'dataprimeiraconsultaclinica': link.dataprimeiraconsultaclinica,
                    'ligacaoconfirmada': link.ligacaoconfirmada,
                    'parceirosexual': link.parceirosexual,
                    'parceirosexualquantos': link.parceirosexualquantos,
                    'filhomenordezanos': link.filhomenordezanos,
                    'filhomenordezanosquantos': link.filhomenordezanosquantos,
                    'maepaiCIPeddezanos': link.maepaiCIPeddezanos,
                    'maepaiCIPeddezanosquantos': link.maepaiCIPeddezanosquantos,
                    'ocupacao': link.ocupacao,
                    'obs': link.obs,
                    'referenciaconselheironome': link.referenciaconselheironome,
                    'sincronizado': link.sincronizado,
                    'ultimasincronizacao': link.ultimasincronizacao,
                    'locationId': link.locationId,
                    'location': link.location.name if link.location else None,
                    'portatestagemId': link.portatestagemId,
                    'portatestagem': link.portatestagem.nome if link.portatestagem else None,
                    'referenciauserId': link.referenciauserId,
                    'referenciauser': link.referenciauser.username if link.referenciauser else None,
                    'userId': link.userId,
                    'user': link.user.username if link.user else None,
                    'keypopulationId': link.keypopulationId,
                    'keypopulation': link.keypopulation.description if link.keypopulation else None,
                    'ligacaocontactosId': link.ligacaocontactosId,
                    'registocontactoId': link.registocontactoId,
                    'createAt': link.createAt,
                    'updateAt': link.updateAt
                }
                return jsonify(result), 200
            return jsonify({'message': 'ContactLink not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            new_link = ContactLink(
                data_sistema=datetime.strptime(data['data_sistema'], '%Y-%m-%d %H:%M:%S'),
                data_registo=datetime.strptime(data['data_registo'], '%Y-%m-%d %H:%M:%S'),
                nomeutente=data['nomeutente'],
                endereco=data['endereco'],
                telefone=data['telefone'],
                nestaus=data['nestaus'],
                outraus=data['outraus'],
                nameustarv=data['nameustarv'],
                nid=data['nid'],
                dataprimeiraconsultaclinica=data['dataprimeiraconsultaclinica'],
                ligacaoconfirmada=data['ligacaoconfirmada'],
                parceirosexual=data['parceirosexual'],
                parceirosexualquantos=data['parceirosexualquantos'],
                filhomenordezanos=data['filhomenordezanos'],
                filhomenordezanosquantos=data['filhomenordezanosquantos'],
                maepaiCIPeddezanos=data['maepaiCIPeddezanos'],
                maepaiCIPeddezanosquantos=data['maepaiCIPeddezanosquantos'],
                ocupacao=data['ocupacao'],
                obs=data['obs'],
                referenciaconselheironome=data['referenciaconselheironome'],
                sincronizado=data['sincronizado'],
                ultimasincronizacao=datetime.strptime(data['ultimasincronizacao'], '%Y-%m-%d %H:%M:%S') if data.get('ultimasincronizacao') else None,
                locationId=data['locationId'],
                portatestagemId=data['portatestagemId'],
                referenciauserId=data['referenciauserId'],
                ligacaocontactosId=data.get('ligacaocontactosId'),
                registocontactoId=data.get('registocontactoId'),
                userId=data['userId'],
                keypopulationId=data['keypopulationId']
            )
            db.session.add(new_link)
            db.session.commit()
            return jsonify({'message': 'Contact link created', 'id': new_link.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            link = ContactLink.query.get(id)
            if not link:
                return jsonify({'message': 'ContactLink not found'}), 404

            db.session.delete(link)
            db.session.commit()
            return jsonify({'message': 'Contact link deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
