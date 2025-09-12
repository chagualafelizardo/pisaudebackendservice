from flask import jsonify, request
from models import db, Textmessage, Grouptype
from datetime import datetime

class TextmessageController:
    @staticmethod
    def get_all():
        try:
            messages = Textmessage.query.all()
            return jsonify([{
                'id': message.id,
                'messagetext': message.messagetext,
                'grouptypeId': message.grouptypeId,
                'grouptype_description': message.grouptype.description if message.grouptype else None,
                'createAt': message.createAt,
                'updateAt': message.updateAt
            } for message in messages]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            message = Textmessage.query.get(id)
            if message:
                return jsonify({
                    'id': message.id,
                    'messagetext': message.messagetext,
                    'grouptypeId': message.grouptypeId,
                    'grouptype_description': message.grouptype.description if message.grouptype else None,
                    'createAt': message.createAt,
                    'updateAt': message.updateAt
                }), 200
            return jsonify({'message': 'Textmessage not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'messagetext' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            if Textmessage.query.filter_by(messagetext=data['messagetext']).first():
                return jsonify({'message': 'Textmessage already exists'}), 400

            # Verificar se o grouptypeId existe (se foi fornecido)
            grouptype_id = data.get('grouptypeId')
            if grouptype_id:
                grouptype = Grouptype.query.get(grouptype_id)
                if not grouptype:
                    return jsonify({'message': 'Grouptype not found'}), 404

            new_message = Textmessage(
                messagetext=data['messagetext'],
                grouptypeId=grouptype_id  # ← AQUI ESTÁ A CORREÇÃO PRINCIPAL
            )

            db.session.add(new_message)
            db.session.commit()

            return jsonify({
                'id': new_message.id,
                'messagetext': new_message.messagetext,
                'grouptypeId': new_message.grouptypeId,  # ← Corrigido: new_message em vez de message
                'grouptype_description': new_message.grouptype.description if new_message.grouptype else None,
                'createAt': new_message.createAt,
                'updateAt': new_message.updateAt
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            message = Textmessage.query.get(id)
            if not message:
                return jsonify({'message': 'Textmessage not found'}), 404

            data = request.get_json()
            if not data or 'messagetext' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            existing = Textmessage.query.filter(
                Textmessage.messagetext == data['messagetext'],
                Textmessage.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Textmessage with this text already exists'}), 400

            # Verificar e atualizar o grouptypeId
            if 'grouptypeId' in data:
                grouptype_id = data['grouptypeId']
                if grouptype_id:
                    grouptype = Grouptype.query.get(grouptype_id)
                    if not grouptype:
                        return jsonify({'message': 'Grouptype not found'}), 404
                message.grouptypeId = grouptype_id

            message.messagetext = data['messagetext']
            message.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': message.id,
                'messagetext': message.messagetext,
                'grouptypeId': message.grouptypeId,
                'grouptype_description': message.grouptype.description if message.grouptype else None,
                'createAt': message.createAt,
                'updateAt': message.updateAt
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            message = Textmessage.query.get(id)
            if not message:
                return jsonify({'message': 'Textmessage not found'}), 404

            db.session.delete(message)
            db.session.commit()

            return jsonify({'message': 'Textmessage deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500