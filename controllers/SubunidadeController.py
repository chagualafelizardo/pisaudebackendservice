import logging
from flask import jsonify, request
from models import db, Subunidade, Resource
from datetime import datetime

logger = logging.getLogger(__name__)

class SubunidadeController:
    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Fetching all subunidades")
            subunidades = Subunidade.query.all()
            result = []
            for sub in subunidades:
                resources_data = []
                for resource in sub.resources:
                    link = db.session.execute(
                        db.select(db.literal_column('quantity'))
                        .select_from(Subunidade.resources.property.secondary)
                        .where(
                            (Subunidade.resources.property.secondary.c.subunidade_id == sub.id) &
                            (Subunidade.resources.property.secondary.c.resource_id == resource.id)
                        )
                    ).fetchone()
                    resources_data.append({
                        'id': resource.id,
                        'name': resource.name,
                        'description': resource.description,
                        'quantity': link[0] if link else 0
                    })

                result.append({
                    'id': sub.id,
                    'name': sub.name,
                    'description': sub.description,
                    'latitude': sub.latitude,
                    'longitude': sub.longitude,
                    'resources': resources_data,
                    'createAt': sub.createAt,
                    'updateAt': sub.updateAt
                })
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"[GET ALL] Failed to fetch subunidades: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"[GET BY ID] Fetching subunidade ID: {id}")
            sub = Subunidade.query.get(id)
            if not sub:
                logger.warning(f"[GET BY ID] Subunidade ID {id} not found")
                return jsonify({'message': 'Subunidade not found'}), 404

            resources_data = []
            for resource in sub.resources:
                link = db.session.execute(
                    db.select([db.literal_column('quantity')])
                    .select_from(Subunidade.resources.property.secondary)
                    .where(
                        (Subunidade.resources.property.secondary.c.subunidade_id == sub.id) &
                        (Subunidade.resources.property.secondary.c.resource_id == resource.id)
                    )
                ).fetchone()
                resources_data.append({
                    'id': resource.id,
                    'name': resource.name,
                    'description': resource.description,
                    'quantity': link[0] if link else 0
                })

            return jsonify({
                'id': sub.id,
                'name': sub.name,
                'description': sub.description,
                'latitude': sub.latitude,
                'longitude': sub.longitude,
                'resources': resources_data,
                'createAt': sub.createAt,
                'updateAt': sub.updateAt
            }), 200
        except Exception as e:
            logger.error(f"[GET BY ID] Error fetching subunidade ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            resources = data.get('resources', [])

            if not name or not description:
                logger.warning("[CREATE] Missing name or description")
                return jsonify({'message': 'Missing required data'}), 400

            if Subunidade.query.filter_by(name=name).first():
                logger.warning(f"[CREATE] Subunidade '{name}' already exists")
                return jsonify({'message': 'Subunidade already exists'}), 400

            new_sub = Subunidade(
                name=name,
                description=description,
                latitude=float(latitude) if latitude else None,
                longitude=float(longitude) if longitude else None
            )
            db.session.add(new_sub)
            db.session.flush()

            for item in resources:
                res = Resource.query.get(item.get('resourceId'))
                if res:
                    logger.info(f"[CREATE] Adding resource ID {res.id} with quantity {item.get('quantity', 0)} to subunidade '{name}'")
                    db.session.execute(
                        Subunidade.resources.property.secondary.insert().values(
                            subunidade_id=new_sub.id,
                            resource_id=res.id,
                            quantity=item.get('quantity', 0)
                        )
                    )

            db.session.commit()
            logger.info(f"[CREATE] Subunidade '{name}' created successfully with ID {new_sub.id}")
            return jsonify({'message': 'Subunidade created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"[CREATE] Failed to create subunidade: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            sub = Subunidade.query.get(id)
            if not sub:
                logger.warning(f"[UPDATE] Subunidade ID {id} not found")
                return jsonify({'message': 'Subunidade not found'}), 404

            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            resources = data.get('resources', [])

            if not name or not description:
                logger.warning(f"[UPDATE] Missing data for subunidade ID {id}")
                return jsonify({'message': 'Missing required data'}), 400

            if Subunidade.query.filter(Subunidade.name == name, Subunidade.id != id).first():
                logger.warning(f"[UPDATE] Subunidade name '{name}' already used by another subunidade")
                return jsonify({'message': 'Subunidade name already in use'}), 400

            logger.info(f"[UPDATE] Updating subunidade ID {id} with name '{name}'")
            sub.name = name
            sub.description = description
            sub.latitude = float(latitude) if latitude else None
            sub.longitude = float(longitude) if longitude else None
            sub.updateAt = datetime.utcnow()

            db.session.execute(
                Subunidade.resources.property.secondary.delete().where(
                    Subunidade.resources.property.secondary.c.subunidade_id == id
                )
            )

            for item in resources:
                res = Resource.query.get(item.get('resourceId'))
                if res:
                    logger.info(f"[UPDATE] Re-adding resource ID {res.id} with quantity {item.get('quantity', 0)}")
                    db.session.execute(
                        Subunidade.resources.property.secondary.insert().values(
                            subunidade_id=sub.id,
                            resource_id=res.id,
                            quantity=item.get('quantity', 0)
                        )
                    )

            db.session.commit()
            logger.info(f"[UPDATE] Subunidade ID {id} updated successfully")
            return jsonify({'message': 'Subunidade updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[UPDATE] Failed to update subunidade ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            sub = Subunidade.query.get(id)
            if not sub:
                logger.warning(f"[DELETE] Subunidade ID {id} not found")
                return jsonify({'message': 'Subunidade not found'}), 404

            db.session.delete(sub)
            db.session.commit()
            logger.info(f"[DELETE] Subunidade ID {id} deleted successfully")
            return jsonify({'message': 'Subunidade deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[DELETE] Failed to delete subunidade ID {id}: {e}")
            return jsonify({'error': str(e)}), 500
