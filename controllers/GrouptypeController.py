from flask import jsonify, request
from models import db, Grouptype
from datetime import datetime

class GrouptypeController:
    @staticmethod
    def get_all():
        try:
            grouptypes = Grouptype.query.all()
            return jsonify([{
                'id': gtp.id,
                'descriton': gtp.descriton,
                'createAt': gtp.createAt,
                'updateAt': gtp.updateAt
            } for gtp in grouptypes]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            grouptype = Grouptype.query.get(id)
            if grouptype:
                return jsonify({
                    'id': grouptype.id,
                    'descriton': grouptype.descriton,
                    'createAt': grouptype.createAt,
                    'updateAt': grouptype.updateAt
                }), 200
            return jsonify({'message': 'Grouptype not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'descriton' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            if Grouptype.query.filter_by(descriton=data['descriton']).first():
                return jsonify({'message': 'Grouptype already exists'}), 400

            novo_grouptype = Grouptype(
                descriton=data['descriton']
            )

            db.session.add(novo_grouptype)
            db.session.commit()

            return jsonify({
                'id': novo_grouptype.id,
                'descriton': novo_grouptype.descriton,
                'createAt': novo_grouptype.createAt,
                'updateAt': novo_grouptype.updateAt
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            grouptype = Grouptype.query.get(id)
            if not grouptype:
                return jsonify({'message': 'Grouptype not found'}), 404

            data = request.get_json()
            if not data or 'descriton' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            existing = Grouptype.query.filter(
                Grouptype.descriton == data['descriton'],
                Grouptype.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Grouptype with this description already exists'}), 400

            grouptype.descriton = data['descriton']
            grouptype.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': grouptype.id,
                'descriton': grouptype.descriton,
                'createAt': grouptype.createAt,
                'updateAt': grouptype.updateAt
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            grouptype = Grouptype.query.get(id)
            if not grouptype:
                return jsonify({'message': 'Grouptype not found'}), 404

            db.session.delete(grouptype)
            db.session.commit()

            return jsonify({'message': 'Grouptype deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500