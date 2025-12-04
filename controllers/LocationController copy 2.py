import logging
import base64

from flask import jsonify, request
from models import db, Location, Resource, location_resource
from datetime import datetime
from sqlalchemy import select, text, and_

logger = logging.getLogger(__name__)

def decode_if_base64(value):
    """
        Decodifica Base64 somente se value for string base64 válida.
        Se for bytes ou None, retorna diretamente.
    """
    if not value:
        return None
    if isinstance(value, bytes):
        return value
    try:
        return base64.b64decode(value)
    except (base64.binascii.Error, ValueError):
        return value.encode() if isinstance(value, str) else value
    
def encode_if_bytes(value):
    if isinstance(value, bytes):
        return base64.b64encode(value).decode('utf-8')
    return value
  
class LocationController:

        
    @staticmethod
    def get_all():
        try:
            logger.info("[GET ALL] Fetching all locations")

            locations = Location.query.all()
            result = []

            # Função reutilizável para serializar os recursos
            def serialize_resource(link):
                return {
                    'id': link.id,
                    'resource_id': link.resource_id,
                    'name': getattr(link, 'name', None),
                    'description': getattr(link, 'description', None),
                    'recebidopor': getattr(link, 'recebidopor', None),
                    'imagem_principal': getattr(link, 'imagem_principal', None),
                    'imagens': getattr(link, 'imagens', None),
                    'anexospdf': getattr(link, 'anexospdf', None),
                    'datarecepcao': link.datarecepcao.isoformat() if getattr(link, "datarecepcao", None) else None,
                    'quantity': getattr(link, 'quantity', None),
                    'createAt': link.createAt.isoformat() if getattr(link, "createAt", None) else None,
                    'updateAt': link.updateAt.isoformat() if getattr(link, "updateAt", None) else None
                }

            for loc in locations:
                stmt = select(location_resource).where(location_resource.c.location_id == loc.id)
                links = db.session.execute(stmt).fetchall()
                resources_data = [serialize_resource(link) for link in links]

                result.append({
                    'id': loc.id,
                    'name': loc.name,
                    'description': loc.description,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'responsavel': loc.responsavel,
                    'observacoes': loc.observacoes,
                    'resources': resources_data,
                    'createAt': loc.createAt.isoformat() if loc.createAt else None,
                    'updateAt': loc.updateAt.isoformat() if loc.updateAt else None
                })

            return jsonify(result), 200

        except Exception as e:
            logger.error(f"[GET ALL] Failed to fetch locations: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_by_id(id):
        try:
            logger.info(f"[GET BY ID] Fetching location ID: {id}")

            loc = Location.query.get(id)
            if not loc:
                return jsonify({'message': 'Location not found'}), 404

            def serialize_resource(link):
                return {
                    'id': link.id,
                    'resource_id': link.resource_id,
                    'name': getattr(link, 'name', None),
                    'description': getattr(link, 'description', None),
                    'recebidopor': getattr(link, 'recebidopor', None),
                    'imagem_principal': getattr(link, 'imagem_principal', None),
                    'imagens': getattr(link, 'imagens', None),
                    'anexospdf': getattr(link, 'anexospdf', None),
                    'datarecepcao': link.datarecepcao.isoformat() if getattr(link, "datarecepcao", None) else None,
                    'quantity': getattr(link, 'quantity', None),
                    'createAt': link.createAt.isoformat() if getattr(link, "createAt", None) else None,
                    'updateAt': link.updateAt.isoformat() if getattr(link, "updateAt", None) else None
                }

            stmt = select(location_resource).where(location_resource.c.location_id == loc.id)
            links = db.session.execute(stmt).fetchall()
            resources_data = [serialize_resource(link) for link in links]

            return jsonify({
                'id': loc.id,
                'name': loc.name,
                'description': loc.description,
                'latitude': loc.latitude,
                'longitude': loc.longitude,
                'responsavel': loc.responsavel,
                'observacoes': loc.observacoes,
                'resources': resources_data,
                'createAt': loc.createAt.isoformat() if loc.createAt else None,
                'updateAt': loc.updateAt.isoformat() if loc.updateAt else None
            }), 200

        except Exception as e:
            logger.error(f"[GET BY ID] Error fetching location ID {id}: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            responsavel = data.get('responsavel', 'DOD')
            observacoes = data.get('observacoes')
            resources = data.get('resources', [])

            if not name or not description:
                return jsonify({'message': 'Missing required data'}), 400

            if responsavel not in Location.get_responsaveis_permitidos():
                return jsonify({'message': f'Responsável deve ser um dos: {", ".join(Location.get_responsaveis_permitidos())}'}), 400

            if Location.query.filter_by(name=name).first():
                return jsonify({'message': 'Location already exists'}), 400

            new_location = Location(
                name=name,
                description=description,
                latitude=float(latitude) if latitude else None,
                longitude=float(longitude) if longitude else None,
                responsavel=responsavel,
                observacoes=observacoes
            )
            db.session.add(new_location)
            db.session.flush()  # Obter ID da nova Location

            # Inserir recursos
            for resource_data in resources:
                imagem_principal = decode_if_base64(resource_data.get('imagem_principal'))
                imagens = decode_if_base64(resource_data.get('imagens'))
                anexospdf = decode_if_base64(resource_data.get('anexospdf'))

                db.session.execute(
                    location_resource.insert().values(
                        location_id=new_location.id,
                        resource_id=resource_data.get('resource_id'),
                        quantity=resource_data.get('quantity', 0),
                        name=resource_data.get('name', ''),
                        description=resource_data.get('description'),
                        recebidopor=resource_data.get('recebidopor'),
                        imagem_principal=imagem_principal,
                        imagens=imagens,
                        anexospdf=anexospdf,
                        datarecepcao=resource_data.get('datarecepcao')
                    )
                )

            db.session.commit()
            return jsonify({'message': 'Location created successfully'}), 201

        except Exception as e:
            db.session.rollback()
            logger.error(f"[CREATE] Failed to create location: {e}")
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            loc = Location.query.get(id)
            if not loc:
                return jsonify({'message': 'Location not found'}), 404

            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            responsavel = data.get('responsavel')
            observacoes = data.get('observacoes')
            resources = data.get('resources', [])

            if not name or not description:
                return jsonify({'message': 'Missing required data'}), 400

            if responsavel and responsavel not in Location.get_responsaveis_permitidos():
                return jsonify({'message': f'Responsável deve ser um dos: {", ".join(Location.get_responsaveis_permitidos())}'}), 400

            if Location.query.filter(Location.name == name, Location.id != id).first():
                return jsonify({'message': 'Location name already in use'}), 400

            # Atualizar dados da Location
            loc.name = name
            loc.description = description
            loc.latitude = float(latitude) if latitude else None
            loc.longitude = float(longitude) if longitude else None
            if responsavel:
                loc.responsavel = responsavel
            loc.observacoes = observacoes
            loc.updateAt = datetime.utcnow()

            # Remover todos os recursos atuais
            db.session.execute(location_resource.delete().where(location_resource.c.location_id == loc.id))

            # Inserir novamente com os dados atualizados
            for resource_data in resources:
                imagem_principal = decode_if_base64(resource_data.get('imagem_principal'))
                imagens = decode_if_base64(resource_data.get('imagens'))
                anexospdf = decode_if_base64(resource_data.get('anexospdf'))

                db.session.execute(
                    location_resource.insert().values(
                        location_id=loc.id,
                        resource_id=resource_data.get('resource_id'),
                        quantity=resource_data.get('quantity', 0),
                        name=resource_data.get('name', ''),
                        description=resource_data.get('description'),
                        recebidopor=resource_data.get('recebidopor'),
                        imagem_principal=imagem_principal,
                        imagens=imagens,
                        anexospdf=anexospdf,
                        datarecepcao=resource_data.get('datarecepcao')
                    )
                )

            db.session.commit()
            return jsonify({'message': 'Location updated successfully'}), 200

        except Exception as e:
            db.session.rollback()
            logger.error(f"[UPDATE] Failed to update location ID {id}: {e}")
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def delete(id):
        try:
            loc = Location.query.get(id)
            if not loc:
                return jsonify({'message': 'Location not found'}), 404

            # 🔹 REMOVER PRIMEIRO OS RECURSOS ASSOCIADOS
            db.session.execute(
                location_resource.delete().where(
                    location_resource.c.location_id == id
                )
            )

            db.session.delete(loc)
            db.session.commit()
            return jsonify({'message': 'Location deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def get_responsaveis():
        try:
            responsaveis = Location.get_responsaveis_permitidos()
            return jsonify({'responsaveis': responsaveis, 'total': len(responsaveis)}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # 🔹 NOVO MÉTODO: ATUALIZAR APENAS UM RECURSO ESPECÍFICO
    @staticmethod
    def update_resource(location_id, resource_id):
        try:
            data = request.get_json()
            
            # 🔹 VERIFICAR SE O REGISTRO EXISTE
            stmt = select(location_resource).where(
                and_(
                    location_resource.c.location_id == location_id,
                    location_resource.c.resource_id == resource_id
                )
            )
            existing = db.session.execute(stmt).fetchone()
            
            if not existing:
                return jsonify({'message': 'Resource not found in this location'}), 404

            # 🔹 ATUALIZAR O REGISTRO
            update_stmt = location_resource.update().where(
                and_(
                    location_resource.c.location_id == location_id,
                    location_resource.c.resource_id == resource_id
                )
            ).values(
                quantity=data.get('quantity', existing.quantity),
                name=data.get('name', existing.name),
                description=data.get('description', existing.description),
                recebidopor=data.get('recebidopor', existing.recebidopor),
                imagem_principal=data.get('imagem_principal', existing.imagem_principal),
                imagens=data.get('imagens', existing.imagens),
                anexospdf=data.get('anexospdf', existing.anexospdf),
                datarecepcao=data.get('datarecepcao', existing.datarecepcao),
                updateAt=datetime.utcnow()
            )

            db.session.execute(update_stmt)
            db.session.commit()

            return jsonify({'message': 'Resource updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[UPDATE RESOURCE] Failed to update resource {resource_id} in location {location_id}: {e}")
            return jsonify({'error': str(e)}), 500

    # 🔹 NOVO MÉTODO: REMOVER APENAS UM RECURSO ESPECÍFICO
    @staticmethod
    def delete_resource(location_id, resource_id):
        try:
            delete_stmt = location_resource.delete().where(
                and_(
                    location_resource.c.location_id == location_id,
                    location_resource.c.resource_id == resource_id
                )
            )
            result = db.session.execute(delete_stmt)
            db.session.commit()

            if result.rowcount == 0:
                return jsonify({'message': 'Resource not found in this location'}), 404

            return jsonify({'message': 'Resource removed from location successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"[DELETE RESOURCE] Failed to delete resource {resource_id} from location {location_id}: {e}")
            return jsonify({'error': str(e)}), 500