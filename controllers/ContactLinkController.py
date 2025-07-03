from flask import jsonify, request
from models import db
from models.ContactLink import ContactLink
from datetime import datetime

class ContactLinkController:
    @staticmethod
    def get_all():
        try:
            contact_links = ContactLink.query.all()
            result = [link.__dict__ for link in contact_links]
            for r in result:
                r.pop('_sa_instance_state', None)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            link = ContactLink.query.get(id)
            if link:
                result = link.__dict__
                result.pop('_sa_instance_state', None)
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
                ultimasincronizacao=data['ultimasincronizacao'],
                locationId=data['locationId'],
                portatestagemId=data['portatestagemId'],
                referenciauserId=data['referenciauserId'],
                ligacaocontactosId=data['ligacaocontactosId'],
                registocontactoId=data['registocontactoId'],
                userId=data['userId']
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
