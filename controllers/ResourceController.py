from flask import jsonify, request
from models import db, Resource, ResourceType
from datetime import datetime

class ResourceController:
    @staticmethod
    def get_all():
        try:
            resources = Resource.query.all()
            return jsonify([
                {
                    'id': res.id,
                    'name': res.name,
                    'description': res.description,
                    'resourcetypeId': res.resourcetypeId,
                    'resourcetypeName': res.resourcetype.name if res.resourcetype else None,
                    'createAt': res.createAt,
                    'updateAt': res.updateAt
                } for res in resources
            ]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            res = Resource.query.get(id)
            if res:
                return jsonify({
                    'id': res.id,
                    'name': res.name,
                    'description': res.description,
                    'resourcetypeId': res.resourcetypeId,
                    'resourcetypeName': res.resourcetype.name if res.resourcetype else None,
                    'createAt': res.createAt,
                    'updateAt': res.updateAt
                }), 200
            return jsonify({'message': 'Resource not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            resourcetypeId = data.get('resourcetypeId')

            if not all([name, resourcetypeId]):
                return jsonify({'message': 'Missing required fields'}), 400

            if Resource.query.filter_by(name=name).first():
                return jsonify({'message': 'Resource already exists'}), 400

            new_resource = Resource(
                name=name,
                description=description,
                resourcetypeId=resourcetypeId
            )
            db.session.add(new_resource)
            db.session.commit()

            return jsonify({'message': 'Resource created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            res = Resource.query.get(id)
            if not res:
                return jsonify({'message': 'Resource not found'}), 404

            data = request.get_json()
            res.name = data.get('name', res.name)
            res.description = data.get('description', res.description)
            res.resourcetypeId = data.get('resourcetypeId', res.resourcetypeId)
            res.updateAt = datetime.utcnow()

            db.session.commit()
            return jsonify({'message': 'Resource updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            res = Resource.query.get(id)
            if not res:
                return jsonify({'message': 'Resource not found'}), 404

            db.session.delete(res)
            db.session.commit()
            return jsonify({'message': 'Resource deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
