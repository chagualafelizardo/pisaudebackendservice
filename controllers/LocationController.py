from flask import jsonify, request
from models import db, Location
from datetime import datetime

class LocationController:
    @staticmethod
    def get_all():
        try:
            locations = Location.query.all()
            return jsonify([{
                'id': loc.id,
                'name': loc.name,
                'createAt': loc.createAt,
                'updateAt': loc.updateAt
            } for loc in locations]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            location = Location.query.get(id)
            if location:
                return jsonify({
                    'id': location.id,
                    'name': location.name,
                    'createAt': location.createAt,
                    'updateAt': location.updateAt
                }), 200
            return jsonify({'message': 'Location not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'name' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            if Location.query.filter_by(name=data['name']).first():
                return jsonify({'message': 'Location already exists'}), 400

            new_location = Location(
                name=data['name']
            )

            db.session.add(new_location)
            db.session.commit()

            return jsonify({
                'id': new_location.id,
                'name': new_location.name,
                'createAt': new_location.createAt,
                'updateAt': new_location.updateAt
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            location = Location.query.get(id)
            if not location:
                return jsonify({'message': 'Location not found'}), 404

            data = request.get_json()
            if not data or 'name' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            existing = Location.query.filter(
                Location.name == data['name'],
                Location.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Location with this name already exists'}), 400

            location.name = data['name']
            location.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': location.id,
                'name': location.name,
                'createAt': location.createAt,
                'updateAt': location.updateAt
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            location = Location.query.get(id)
            if not location:
                return jsonify({'message': 'Location not found'}), 404

            db.session.delete(location)
            db.session.commit()

            return jsonify({'message': 'Location deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500