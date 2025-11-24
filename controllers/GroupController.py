from flask import jsonify, request
from models import Observation, db, Group
from datetime import datetime

class GroupController:

    @staticmethod
    def get_all():
        try:
            groups = Group.query.all()
            return jsonify([{
                'id': group.id,
                'description': group.description,
                'dateStart': group.dateStart.strftime('%Y-%m-%d') if group.dateStart else None,
                'dateEnd': group.dateEnd.strftime('%Y-%m-%d') if group.dateEnd else None,
                'observation': group.observation,
                'createAt': group.createAt,
                'updateAt': group.updateAt
            } for group in groups]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def get_by_id(id):
        try:
            group = Group.query.get(id)
            if group:
                return jsonify({
                    'id': group.id,
                    'description': group.description,
                    'dateStart': group.dateStart.strftime('%Y-%m-%d') if group.dateStart else None,
                    'dateEnd': group.dateEnd.strftime('%Y-%m-%d') if group.dateEnd else None,
                    'observation': group.observation,
                    'createAt': group.createAt,
                    'updateAt': group.updateAt
                }), 200
            return jsonify({'message': 'group not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            if Group.query.filter_by(description=data['description']).first():
                return jsonify({'message': 'Group already exists'}), 400

            new_group = Group(
                description=data['description'],
                dateStart=datetime.strptime(data.get('dateStart'), '%Y-%m-%d') if data.get('dateStart') else None,
                dateEnd=datetime.strptime(data.get('dateEnd'), '%Y-%m-%d') if data.get('dateEnd') else None,
                observation=data.get('observation')
            )

            db.session.add(new_group)
            db.session.commit()

            return jsonify({'message': 'Group created successfully', 'id': new_group.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def update(id):
        try:
            group = Group.query.get(id)
            if not group:
                return jsonify({'message': 'group not found'}), 404

            data = request.get_json()
            if not data or 'description' not in data:
                return jsonify({'message': 'Missing required data'}), 400

            existing = Group.query.filter(
                Group.description == data['description'],
                Group.id != id
            ).first()
            if existing:
                return jsonify({'message': 'Group with this description already exists'}), 400

            group.description = data['description']
            group.dateStart = datetime.strptime(data.get('dateStart'), '%Y-%m-%d') if data.get('dateStart') else None
            group.dateEnd = datetime.strptime(data.get('dateEnd'), '%Y-%m-%d') if data.get('dateEnd') else None
            group.observation = data.get('observation')
            group.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({'message': 'Group updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def add_members():
        try:
            data = request.get_json()
            print("Received data:", data)  # <-- debug
            group_id = data.get('groupId') if data else None
            patients = data.get('patients', []) if data else []

            if not group_id or not patients:
                return jsonify({"error": "Invalid data"}), 400

            for pid in patients:
                obs = Observation.query.get(pid)
                if obs:
                    obs.groupId = group_id

            db.session.commit()
            return jsonify({"message": "Members added successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            group = Group.query.get(id)
            if not group:
                return jsonify({'message': 'group not found'}), 404

            db.session.delete(group)
            db.session.commit()

            return jsonify({'message': 'group deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
