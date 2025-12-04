import logging
from flask import jsonify, request
from models import db, LocationResource
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LocationResourceController:

    @staticmethod
    def serialize(obj: LocationResource):
        return {
            'id': obj.id,
            'location_id': obj.location_id,
            'name': obj.name,
            'description': obj.description,
            'recebidopor': obj.recebidopor,

            # 🔹 NOVO
            'imagem_principal': obj.imagem_principal,
            'imagens': obj.imagens,

            'anexospdf': obj.anexospdf,
            'datarecepcao': obj.datarecepcao.isoformat() if obj.datarecepcao else None,
            'quantidade': obj.quantidade,
            'createAt': obj.createAt.isoformat() if obj.createAt else None,
            'updateAt': obj.updateAt.isoformat() if obj.updateAt else None
        }

    # 🔹 GET ALL
    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Fetching all LocationResources")
            items = LocationResource.query.all()
            return jsonify([LocationResourceController.serialize(i) for i in items]), 200
        except Exception as e:
            logger.exception("[GET ALL] Failed to fetch")
            return jsonify({'error': str(e)}), 500

    # 🔹 GET by ID
    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"[GET BY ID] Fetching LocationResource ID {id}")
            item = LocationResource.query.get(id)
            if not item:
                return jsonify({'message': 'LocationResource not found'}), 404
            return jsonify(LocationResourceController.serialize(item)), 200
        except Exception as e:
            logger.exception(f"[GET BY ID] Failed to fetch ID {id}")
            return jsonify({'error': str(e)}), 500

    # 🔹 CREATE
    @staticmethod
    def create():
        try:
            data = request.get_json()
            logger.info("[CREATE] Data received: %s", data)

            required_fields = ['location_id', 'name']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'message': f'{field} is required'}), 400

            item = LocationResource(
                location_id=data.get('location_id'),
                name=data.get('name'),
                description=data.get('description'),
                recebidopor=data.get('recebidopor'),

                # 🔥 NOVOS CAMPOS
                imagem_principal=data.get('imagem_principal'),
                imagens=data.get('imagens'),

                anexospdf=data.get('anexospdf'),
                datarecepcao=data.get('datarecepcao'),
                quantidade=data.get('quantidade', 0)
            )

            db.session.add(item)
            db.session.commit()

            return jsonify({
                'message': 'LocationResource created successfully',
                'data': LocationResourceController.serialize(item)
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.exception("[CREATE] Failed to create")
            return jsonify({'error': str(e)}), 500

    # 🔹 UPDATE
    @staticmethod
    def update(id):
        try:
            logger.info(f"[UPDATE] Updating LocationResource ID {id}")
            item = LocationResource.query.get(id)
            if not item:
                return jsonify({'message': 'LocationResource not found'}), 404

            data = request.get_json()
            logger.info(f"[UPDATE] Data received: {data}")

            item.location_id = data.get('location_id', item.location_id)
            item.name = data.get('name', item.name)
            item.description = data.get('description', item.description)
            item.recebidopor = data.get('recebidopor', item.recebidopor)

            # 🔥 NOVOS CAMPOS
            item.imagem_principal = data.get('imagem_principal', item.imagem_principal)
            item.imagens = data.get('imagens', item.imagens)

            item.anexospdf = data.get('anexospdf', item.anexospdf)
            item.datarecepcao = data.get('datarecepcao', item.datarecepcao)
            item.quantidade = data.get('quantidade', item.quantidade)

            item.updateAt = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'LocationResource updated successfully',
                'data': LocationResourceController.serialize(item)
            }), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[UPDATE] Failed to update ID {id}")
            return jsonify({'error': str(e)}), 500

    # 🔹 DELETE
    @staticmethod
    def delete(id):
        try:
            logger.info(f"[DELETE] Deleting LocationResource ID {id}")
            item = LocationResource.query.get(id)
            if not item:
                return jsonify({'message': 'LocationResource not found'}), 404

            db.session.delete(item)
            db.session.commit()

            return jsonify({'message': 'LocationResource deleted successfully'}), 200

        except Exception as e:
            db.session.rollback()
            logger.exception(f"[DELETE] Failed to delete ID {id}")
            return jsonify({'error': str(e)}), 500
