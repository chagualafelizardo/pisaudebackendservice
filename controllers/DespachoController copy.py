# import logging
# import traceback
# from flask import jsonify, request, send_file
# from io import BytesIO
# from datetime import datetime
# from models import db, Despacho, EstadoDespachoEnum, Person
# import base64

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# class DespachoController:

#     @staticmethod
#     def get_all():
#         try:
#             logger.info("[GET ALL] Iniciando busca de todos os despachos")
#             despachos = Despacho.query.all()
#             result = []
#             for d in despachos:
#                 result.append({
#                     'id': d.id,
#                     'person_id': d.person_id,
#                     'person_image': base64.b64encode(d.person.image).decode('utf-8') if d.person and d.person.image else None,
#                     'person': {
#                             'id': d.person.id if d.person else None,
#                             'fullname': d.person.fullname if d.person else None,
#                             'nim': d.person.nim if d.person else None,
#                             'gender': d.person.gender if d.person else None,
#                             'dateofbirth': d.person.dateofbirth.isoformat() if d.person and d.person.dateofbirth else None,
#                             'dataIncorporacao': d.person.incorporationdata.isoformat() if d.person and d.person.incorporationdata else None,
#                             'image': base64.b64encode(d.person.image).decode('utf-8') if d.person and d.person.image else None
#                         } if d.person else None,
#                     'titulo': d.titulo,
#                     'descricao': d.descricao,
#                     'data_despacho': d.data_despacho.isoformat() if d.data_despacho else None,
#                     'estado': d.estado.value,
#                     'observacao': d.observacao,
#                     'anexo_nome': d.anexo_nome,
#                     'criado_em': d.criado_em.isoformat() if d.criado_em else None,
#                     'atualizado_em': d.atualizado_em.isoformat() if d.atualizado_em else None
#                 })
            
#             logger.info(f"[GET ALL] Encontrados {len(result)} despachos")
#             return jsonify(result), 200
            
#         except Exception as e:
#             logger.exception(f"[GET ALL] ERRO CRÍTICO ao listar despachos: {str(e)}")
#             return jsonify({'error': 'Erro interno do servidor ao buscar despachos'}), 500

#     @staticmethod
#     def get_by_id(id):
#         try:
#             logger.info(f"[GET BY ID] Buscando despacho ID: {id}")
#             d = Despacho.query.get(id)
#             if not d:
#                 logger.warning(f"[GET BY ID] Despacho não encontrado: {id}")
#                 return jsonify({'message': 'Despacho não encontrado'}), 404

#             result = {
#                 'id': d.id,
#                 'person_id': d.person_id,
#                 'person': {
#                     'id': d.person.id if d.person else None,
#                     'fullname': d.person.fullname if d.person else None,
#                     'nim': d.person.nim if d.person else None,
#                     'gender': d.person.gender if d.person else None,
#                     'dateofbirth': d.person.dateofbirth.isoformat() if d.person and d.person.dateofbirth else None,
#                     'dataIncorporacao': d.person.incorporationdata.isoformat() if d.person and d.person.incorporationdata else None,
#                     'image': d.person.image if d.person else None
#                 } if d.person else None,
#                 'titulo': d.titulo,
#                 'descricao': d.descricao,
#                 'data_despacho': d.data_despacho.isoformat() if d.data_despacho else None,
#                 'estado': d.estado.value,
#                 'observacao': d.observacao,
#                 'anexo_nome': d.anexo_nome,
#                 'anexo_tipo': d.anexo_tipo,
#                 'criado_em': d.criado_em.isoformat() if d.criado_em else None,
#                 'atualizado_em': d.atualizado_em.isoformat() if d.atualizado_em else None
#             }
            
#             logger.info(f"[GET BY ID] Despacho encontrado: {d.titulo}")
#             return jsonify(result), 200
            
#         except Exception as e:
#             logger.exception(f"[GET BY ID] ERRO ao buscar despacho {id}: {str(e)}")
#             return jsonify({'error': f'Erro ao buscar despacho: {str(e)}'}), 500

#     @staticmethod
#     def create():
#         try:
#             # Verificar se é multipart/form-data
#             if not request.content_type or 'multipart/form-data' not in request.content_type:
#                 logger.warning("[CREATE] Content-Type não é multipart/form-data")
#                 return jsonify({'error': 'Content-Type deve ser multipart/form-data'}), 400

#             data = request.form.to_dict()
#             file = request.files.get('anexo')
            
#             logger.info(f"[CREATE] Iniciando criação de despacho. Dados recebidos: {list(data.keys())}")
#             logger.info(f"[CREATE] Ficheiro anexo: {'Sim' if file else 'Não'}")

#             titulo = data.get('titulo', '').strip()
#             if not titulo:
#                 logger.warning("[CREATE] Tentativa de criar despacho sem título")
#                 return jsonify({'error': 'O campo título é obrigatório'}), 400

#             # Processar data do despacho
#             data_despacho_str = data.get('data_despacho')
#             data_despacho = None
#             if data_despacho_str:
#                 try:
#                     data_despacho = datetime.strptime(data_despacho_str, '%Y-%m-%d').date()
#                     logger.info(f"[CREATE] Data do despacho: {data_despacho}")
#                 except ValueError as e:
#                     logger.warning(f"[CREATE] Data inválida: {data_despacho_str}. Usando data atual.")
#                     data_despacho = datetime.now().date()
#             else:
#                 data_despacho = datetime.now().date()

#             # Processar estado
#             estado_str = data.get('estado', 'PENDENTE')
#             try:
#                 estado = EstadoDespachoEnum[estado_str]
#                 logger.info(f"[CREATE] Estado do despacho: {estado.value}")
#             except KeyError:
#                 logger.warning(f"[CREATE] Estado inválido: {estado_str}. Usando PENDENTE.")
#                 estado = EstadoDespachoEnum.PENDENTE

#             # Processar person_id
#             person_id = data.get('person_id')
#             if person_id:
#                 try:
#                     person_id = int(person_id)
#                     # Verificar se a pessoa existe
#                     person = Person.query.get(person_id)
#                     if not person:
#                         logger.warning(f"[CREATE] Person ID não encontrado: {person_id}")
#                         return jsonify({'error': f'Militar com ID {person_id} não encontrado'}), 400
#                     logger.info(f"[CREATE] Person ID válido: {person_id}")
#                 except (ValueError, TypeError):
#                     logger.warning(f"[CREATE] Person ID inválido: {person_id}. Definindo como None.")
#                     person_id = None

#             # Criar o despacho
#             novo_despacho = Despacho(
#                 titulo=titulo,
#                 descricao=data.get('descricao', '').strip(),
#                 data_despacho=data_despacho,
#                 estado=estado,
#                 observacao=data.get('observacao', '').strip(),
#                 person_id=person_id
#             )

#             # Processar anexo
#             if file and file.filename:
#                 logger.info(f"[CREATE] Processando anexo: {file.filename} ({file.mimetype})")
#                 if file.content_length and file.content_length > 10 * 1024 * 1024:  # 10MB limit
#                     return jsonify({'error': 'Ficheiro muito grande. Máximo 10MB permitido.'}), 400
                
#                 novo_despacho.anexo_nome = file.filename
#                 novo_despacho.anexo_tipo = file.mimetype
#                 novo_despacho.anexo_dados = file.read()
#                 logger.info(f"[CREATE] Anexo processado com sucesso - Tamanho: {len(novo_despacho.anexo_dados)} bytes")

#             db.session.add(novo_despacho)
#             db.session.commit()
            
#             logger.info(f"[CREATE] Despacho criado com sucesso. ID: {novo_despacho.id}")
#             return jsonify({
#                 'message': 'Despacho criado com sucesso', 
#                 'id': novo_despacho.id,
#                 'titulo': novo_despacho.titulo
#             }), 201
            
#         except Exception as e:
#             db.session.rollback()
#             error_msg = f"[CREATE] ERRO CRÍTICO ao criar despacho: {str(e)}"
#             logger.exception(error_msg)
#             return jsonify({'error': 'Erro interno do servidor ao criar despacho'}), 500

#     @staticmethod
#     def update(id):
#         try:
#             logger.info(f"[UPDATE] Iniciando atualização do despacho ID: {id}")
            
#             # Verificar se é multipart/form-data
#             if not request.content_type or 'multipart/form-data' not in request.content_type:
#                 logger.warning("[UPDATE] Content-Type não é multipart/form-data")
#                 return jsonify({'error': 'Content-Type deve ser multipart/form-data'}), 400

#             despacho = Despacho.query.get(id)
#             if not despacho:
#                 logger.warning(f"[UPDATE] Despacho não encontrado: {id}")
#                 return jsonify({'error': 'Despacho não encontrado'}), 404

#             data = request.form.to_dict()
#             file = request.files.get('anexo')
            
#             logger.info(f"[UPDATE] Dados recebidos: {list(data.keys())}")
#             logger.info(f"[UPDATE] Ficheiro anexo: {'Sim' if file else 'Não'}")

#             # Atualizar campos
#             if 'titulo' in data:
#                 titulo = data['titulo'].strip()
#                 if not titulo:
#                     return jsonify({'error': 'O campo título é obrigatório'}), 400
#                 despacho.titulo = titulo
                
#             if 'descricao' in data:
#                 despacho.descricao = data['descricao'].strip()
                
#             if 'data_despacho' in data and data['data_despacho']:
#                 try:
#                     despacho.data_despacho = datetime.strptime(data['data_despacho'], '%Y-%m-%d').date()
#                 except ValueError:
#                     logger.warning(f"[UPDATE] Data inválida: {data['data_despacho']}")
#                     return jsonify({'error': 'Data inválida'}), 400
                    
#             if 'estado' in data:
#                 try:
#                     despacho.estado = EstadoDespachoEnum[data['estado']]
#                 except KeyError:
#                     logger.warning(f"[UPDATE] Estado inválido: {data['estado']}")
#                     return jsonify({'error': 'Estado inválido'}), 400
                    
#             if 'observacao' in data:
#                 despacho.observacao = data['observacao'].strip()
                
#             if 'person_id' in data:
#                 person_id = data['person_id']
#                 if person_id:
#                     try:
#                         person_id = int(person_id)
#                         person = Person.query.get(person_id)
#                         if not person:
#                             return jsonify({'error': f'Militar com ID {person_id} não encontrado'}), 400
#                         despacho.person_id = person_id
#                     except (ValueError, TypeError):
#                         despacho.person_id = None
#                 else:
#                     despacho.person_id = None

#             # Processar anexo se fornecido
#             if file and file.filename:
#                 logger.info(f"[UPDATE] Atualizando anexo: {file.filename}")
#                 if file.content_length and file.content_length > 10 * 1024 * 1024:  # 10MB limit
#                     return jsonify({'error': 'Ficheiro muito grande. Máximo 10MB permitido.'}), 400
                    
#                 despacho.anexo_nome = file.filename
#                 despacho.anexo_tipo = file.mimetype
#                 despacho.anexo_dados = file.read()

#             db.session.commit()
#             logger.info(f"[UPDATE] Despacho atualizado com sucesso: {id}")
            
#             return jsonify({
#                 'message': 'Despacho atualizado com sucesso',
#                 'id': despacho.id
#             }), 200
            
#         except Exception as e:
#             db.session.rollback()
#             error_msg = f"[UPDATE] ERRO ao atualizar despacho {id}: {str(e)}"
#             logger.exception(error_msg)
#             return jsonify({'error': 'Erro interno do servidor ao atualizar despacho'}), 500

#     @staticmethod
#     def delete(id):
#         try:
#             logger.info(f"[DELETE] Iniciando exclusão do despacho ID: {id}")
#             despacho = Despacho.query.get(id)
#             if not despacho:
#                 logger.warning(f"[DELETE] Despacho não encontrado: {id}")
#                 return jsonify({'error': 'Despacho não encontrado'}), 404

#             db.session.delete(despacho)
#             db.session.commit()
            
#             logger.info(f"[DELETE] Despacho excluído com sucesso: {id}")
#             return jsonify({'message': 'Despacho excluído com sucesso'}), 200
            
#         except Exception as e:
#             db.session.rollback()
#             error_msg = f"[DELETE] ERRO ao excluir despacho {id}: {str(e)}"
#             logger.exception(error_msg)
#             return jsonify({'error': 'Erro interno do servidor ao excluir despacho'}), 500

#     @staticmethod
#     def download_anexo(id):
#         try:
#             logger.info(f"[DOWNLOAD ANEXO] Solicitado anexo do despacho: {id}")
#             despacho = Despacho.query.get(id)
#             if not despacho:
#                 logger.warning(f"[DOWNLOAD ANEXO] Despacho não encontrado: {id}")
#                 return jsonify({'error': 'Despacho não encontrado'}), 404

#             if not despacho.anexo_dados:
#                 logger.warning(f"[DOWNLOAD ANEXO] Anexo não encontrado para despacho: {id}")
#                 return jsonify({'error': 'Anexo não encontrado'}), 404

#             logger.info(f"[DOWNLOAD ANEXO] Enviando anexo: {despacho.anexo_nome}")
#             return send_file(
#                 BytesIO(despacho.anexo_dados),
#                 as_attachment=True,
#                 download_name=despacho.anexo_nome,
#                 mimetype=despacho.anexo_tipo or 'application/octet-stream'
#             )
            
#         except Exception as e:
#             logger.exception(f"[DOWNLOAD ANEXO] ERRO ao baixar anexo {id}: {str(e)}")
#             return jsonify({'error': 'Erro interno do servidor ao baixar anexo'}), 500