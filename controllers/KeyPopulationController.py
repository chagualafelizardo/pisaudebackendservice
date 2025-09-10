from flask import jsonify, request
from models import db, keyPopulation
from datetime import datetime

class KeyPopulationController:
    @staticmethod
    def get_all():
        try:
            populations = keyPopulation.query.all()
            return jsonify([{
                'id': pop.id,
                'description': pop.description,
                'createAt': pop.createAt.isoformat() if pop.createAt else None,
                'updateAt': pop.updateAt.isoformat() if pop.updateAt else None
            } for pop in populations]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            population = keyPopulation.query.get(id)
            if population:
                return jsonify({
                    'id': population.id,
                    'description': population.description,
                    'createAt': population.createAt.isoformat() if population.createAt else None,
                    'updateAt': population.updateAt.isoformat() if population.updateAt else None
                }), 200
            return jsonify({'message': 'Key population not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data (description)'}), 400

            if keyPopulation.query.filter_by(description=data['description']).first():
                return jsonify({'message': 'Key population with this description already exists'}), 400

            new_population = keyPopulation(
                description=data['description']
            )

            db.session.add(new_population)
            db.session.commit()

            return jsonify({
                'id': new_population.id,
                'description': new_population.description,
                'createAt': new_population.createAt.isoformat(),
                'updateAt': new_population.updateAt.isoformat()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            population = keyPopulation.query.get(id)
            if not population:
                return jsonify({'message': 'Key population not found'}), 404

            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data (description)'}), 400

            existing = keyPopulation.query.filter(
                keyPopulation.description == data['description'],
                keyPopulation.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Key population with this description already exists'}), 400

            population.description = data['description']
            population.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'id': population.id,
                'description': population.description,
                'createAt': population.createAt.isoformat(),
                'updateAt': population.updateAt.isoformat()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            population = keyPopulation.query.get(id)
            if not population:
                return jsonify({'message': 'Key population not found'}), 404

            db.session.delete(population)
            db.session.commit()

            return jsonify({'message': 'Key population deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500