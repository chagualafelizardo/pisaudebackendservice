# import logging
# from flask import jsonify, request
# from models import db, Location, Resource
# from datetime import datetime
# from sqlalchemy import select, text

# logger = logging.getLogger(__name__)

# class LocationController:
#     @staticmethod
#     def get_all():
#         try:
#             logger.info("[GET ALL] Fetching all locations")
#             locations = Location.query.all()
#             result = []
#             for loc in locations:
#                 resources_data = []
#                 for resource in loc.resources:
#                     stmt = select(text('quantity')).select_from(
#                         Location.resources.property.secondary
#                     ).where(
#                         (Location.resources.property.secondary.c.location_id == loc.id) &
#                         (Location.resources.property.secondary.c.resource_id == resource.id)
#                     )
#                     link = db.session.execute(stmt).fetchone()
#                     resources_data.append({
#                         'id': resource.id,
#                         'name': resource.name,
#                         'description': resource.description,
#                         'quantity': link[0] if link else 0
#                     })

#                 result.append({
#                     'id': loc.id,
#                     'name': loc.name,
#                     'description': loc.description,
#                     'latitude': loc.latitude,
#                     'longitude': loc.longitude,
#                     'responsavel': loc.responsavel,
#                     'observacoes': loc.observacoes,   # 👇 ADICIONADO
#                     'resources': resources_data,
#                     'createAt': loc.createAt,
#                     'updateAt': loc.updateAt
#                 })
#             return jsonify(result), 200
#         except Exception as e:
#             logger.error(f"[GET ALL] Failed to fetch locations: {e}")
#             return jsonify({'error': str(e)}), 500

#     @staticmethod
#     def get_by_id(id):
#         try:
#             logger.info(f"[GET BY ID] Fetching location ID: {id}")
#             loc = Location.query.get(id)
#             if not loc:
#                 return jsonify({'message': 'Location not found'}), 404

#             resources_data = []
#             for resource in loc.resources:
#                 stmt = select(text('quantity')).select_from(
#                     Location.resources.property.secondary
#                 ).where(
#                     (Location.resources.property.secondary.c.location_id == loc.id) &
#                     (Location.resources.property.secondary.c.resource_id == resource.id)
#                 )
#                 link = db.session.execute(stmt).fetchone()
#                 resources_data.append({
#                     'id': resource.id,
#                     'name': resource.name,
#                     'description': resource.description,
#                     'quantity': link[0] if link else 0
#                 })

#             return jsonify({
#                 'id': loc.id,
#                 'name': loc.name,
#                 'description': loc.description,
#                 'latitude': loc.latitude,
#                 'longitude': loc.longitude,
#                 'responsavel': loc.responsavel,
#                 'observacoes': loc.observacoes,   # 👇 ADICIONADO
#                 'resources': resources_data,
#                 'createAt': loc.createAt,
#                 'updateAt': loc.updateAt
#             }), 200
#         except Exception as e:
#             logger.error(f"[GET BY ID] Error fetching location ID {id}: {e}")
#             return jsonify({'error': str(e)}), 500

#     @staticmethod
#     def create():
#         try:
#             data = request.get_json()
#             name = data.get('name')
#             description = data.get('description')
#             latitude = data.get('latitude')
#             longitude = data.get('longitude')
#             responsavel = data.get('responsavel', 'DOD')
#             observacoes = data.get('observacoes')  # 👇 ADICIONADO
#             resources = data.get('resources', [])

#             if not name or not description:
#                 return jsonify({'message': 'Missing required data'}), 400

#             responsaveis_permitidos = Location.get_responsaveis_permitidos()
#             if responsavel not in responsaveis_permitidos:
#                 return jsonify({'message': f'Responsável deve ser um dos: {", ".join(responsaveis_permitidos)}'}), 400

#             if Location.query.filter_by(name=name).first():
#                 return jsonify({'message': 'Location already exists'}), 400

#             new_location = Location(
#                 name=name,
#                 description=description,
#                 latitude=float(latitude) if latitude else None,
#                 longitude=float(longitude) if longitude else None,
#                 responsavel=responsavel,
#                 observacoes=observacoes   # 👇 ADICIONADO
#             )
#             db.session.add(new_location)
#             db.session.flush()

#             for item in resources:
#                 res = Resource.query.get(item.get('resourceId'))
#                 if res:
#                     db.session.execute(
#                         Location.resources.property.secondary.insert().values(
#                             location_id=new_location.id,
#                             resource_id=res.id,
#                             quantity=item.get('quantity', 0)
#                         )
#                     )

#             db.session.commit()
#             return jsonify({'message': 'Location created successfully'}), 201
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f"[CREATE] Failed to create location: {e}")
#             return jsonify({'error': str(e)}), 500

#     @staticmethod
#     def update(id):
#         try:
#             loc = Location.query.get(id)
#             if not loc:
#                 return jsonify({'message': 'Location not found'}), 404

#             data = request.get_json()
#             name = data.get('name')
#             description = data.get('description')
#             latitude = data.get('latitude')
#             longitude = data.get('longitude')
#             responsavel = data.get('responsavel')
#             observacoes = data.get('observacoes')  # 👇 ADICIONADO
#             resources = data.get('resources', [])

#             if not name or not description:
#                 return jsonify({'message': 'Missing required data'}), 400

#             if responsavel:
#                 responsaveis_permitidos = Location.get_responsaveis_permitidos()
#                 if responsavel not in responsaveis_permitidos:
#                     return jsonify({'message': f'Responsável deve ser um dos: {", ".join(responsaveis_permitidos)}'}), 400

#             if Location.query.filter(Location.name == name, Location.id != id).first():
#                 return jsonify({'message': 'Location name already in use'}), 400

#             loc.name = name
#             loc.description = description
#             loc.latitude = float(latitude) if latitude else None
#             loc.longitude = float(longitude) if longitude else None

#             if responsavel:
#                 loc.responsavel = responsavel

#             loc.observacoes = observacoes  # 👇 ADICIONADO
#             loc.updateAt = datetime.utcnow()

#             db.session.execute(
#                 Location.resources.property.secondary.delete().where(
#                     Location.resources.property.secondary.c.location_id == id
#                 )
#             )

#             for item in resources:
#                 res = Resource.query.get(item.get('resourceId'))
#                 if res:
#                     db.session.execute(
#                         Location.resources.property.secondary.insert().values(
#                             location_id=loc.id,
#                             resource_id=res.id,
#                             quantity=item.get('quantity', 0)
#                         )
#                     )

#             db.session.commit()
#             return jsonify({'message': 'Location updated successfully'}), 200
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f"[UPDATE] Failed to update location ID {id}: {e}")
#             return jsonify({'error': str(e)}), 500

#     @staticmethod
#     def delete(id):
#         try:
#             loc = Location.query.get(id)
#             if not loc:
#                 return jsonify({'message': 'Location not found'}), 404

#             db.session.delete(loc)
#             db.session.commit()
#             return jsonify({'message': 'Location deleted successfully'}), 200
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#     @staticmethod
#     def get_responsaveis():
#         try:
#             responsaveis = Location.get_responsaveis_permitidos()
#             return jsonify({'responsaveis': responsaveis, 'total': len(responsaveis)}), 200
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500
