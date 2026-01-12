# import logging
# import json
# from flask import jsonify, request
# from models import db, Medico, HorarioMedico, Agendamento, SMS, HorarioPadrao, Observation
# from datetime import datetime, date, time, timedelta
# from sqlalchemy import and_, or_, func

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

# class AgendamentoController:

#     # ====================
#     # FUNÇÕES AUXILIARES
#     # ====================
    
#     @staticmethod
#     def serialize_medico(m: Medico):
#         return {
#             'id': m.id,
#             'nome': m.nome,
#             'especialidade': m.especialidade,
#             'registro_profissional': m.registro_profissional,
#             'telefone': m.telefone,
#             'email': m.email,
#             'horario_trabalho': m.horario_trabalho,
#             'ativo': m.ativo,
#             'createAt': m.createAt.isoformat() if m.createAt else None,
#             'updateAt': m.updateAt.isoformat() if m.updateAt else None
#         }

#     @staticmethod
#     def serialize_agendamento(a: Agendamento):
#         medico_nome = a.medico.nome if a.medico else None
        
#         return {
#             'id': a.id,
#             'paciente_id': a.paciente_id,
#             'paciente_nome': a.paciente_nome,
#             'telefone': a.telefone,
#             'medico_id': a.medico_id,
#             'medico_nome': medico_nome,
#             'data_consulta': a.data_consulta.isoformat() if a.data_consulta else None,
#             'hora_consulta': a.hora_consulta.isoformat() if a.hora_consulta else None,
#             'tipo_consulta': a.tipo_consulta,
#             'status': a.status,
#             'observacoes': a.observacoes,
#             'sms_enviado': a.sms_enviado,
#             'sms_confirmacao_enviado': a.sms_confirmacao_enviado,
#             'ultimo_sms_data': a.ultimo_sms_data.isoformat() if a.ultimo_sms_data else None,
#             'createAt': a.createAt.isoformat() if a.createAt else None,
#             'updateAt': a.updateAt.isoformat() if a.updateAt else None
#         }

#     @staticmethod
#     def serialize_sms(s: SMS):
#         return {
#             'id': s.id,
#             'destinatario': s.destinatario,
#             'destinatario_nome': s.destinatario_nome,
#             'mensagem': s.mensagem,
#             'tipo': s.tipo,
#             'status': s.status,
#             'resposta': s.resposta,
#             'mensagem_id': s.mensagem_id,
#             'agendamento_id': s.agendamento_id,
#             'data_envio': s.data_envio.isoformat() if s.data_envio else None,
#             'createAt': s.createAt.isoformat() if s.createAt else None,
#             'updateAt': s.updateAt.isoformat() if s.updateAt else None
#         }

#     @staticmethod
#     def serialize_horario(h: HorarioMedico):
#         return {
#             'id': h.id,
#             'medico_id': h.medico_id,
#             'dia_semana': h.dia_semana,
#             'hora_inicio': h.hora_inicio.isoformat() if h.hora_inicio else None,
#             'hora_fim': h.hora_fim.isoformat() if h.hora_fim else None,
#             'duracao_consulta': h.duracao_consulta,
#             'intervalo_almoco_inicio': h.intervalo_almoco_inicio.isoformat() if h.intervalo_almoco_inicio else None,
#             'intervalo_almoco_fim': h.intervalo_almoco_fim.isoformat() if h.intervalo_almoco_fim else None,
#             'data_especifica': h.data_especifica.isoformat() if h.data_especifica else None,
#             'ativo': h.ativo,
#             'createAt': h.createAt.isoformat() if h.createAt else None,
#             'updateAt': h.updateAt.isoformat() if h.updateAt else None
#         }

#     # ====================
#     # ESTATÍSTICAS
#     # ====================
#     @staticmethod
#     def get_estatisticas():
#         try:
#             hoje = date.today()
            
#             # Agendamentos de hoje
#             hoje_count = Agendamento.query.filter(
#                 Agendamento.data_consulta == hoje
#             ).count()
            
#             # Por status
#             confirmados = Agendamento.query.filter(
#                 Agendamento.status == 'confirmado',
#                 Agendamento.data_consulta >= hoje
#             ).count()
            
#             pendentes = Agendamento.query.filter(
#                 Agendamento.status == 'pendente',
#                 Agendamento.data_consulta >= hoje
#             ).count()
            
#             cancelados = Agendamento.query.filter(
#                 Agendamento.status == 'cancelado',
#                 Agendamento.data_consulta >= hoje
#             ).count()
            
#             return jsonify({
#                 'hoje': hoje_count,
#                 'confirmados': confirmados,
#                 'pendentes': pendentes,
#                 'cancelados': cancelados,
#                 'total': Agendamento.query.count()
#             }), 200
            
#         except Exception as e:
#             logger.exception("[ESTATÍSTICAS] Erro ao buscar estatísticas")
#             return jsonify({'error': str(e)}), 500

#     # ====================
#     # LISTAR AGENDAMENTOS
#     # ====================
#     @staticmethod
#     def listar_agendamentos():
#         try:
#             data = request.get_json() if request.is_json else {}
            
#             # Filtros
#             filtro_data = data.get('data')
#             filtro_medico_id = data.get('medico_id')
#             filtro_status = data.get('status')
#             pagina = data.get('pagina', 1)
#             por_pagina = data.get('por_pagina', 20)
            
#             query = Agendamento.query
            
#             # Aplicar filtros
#             if filtro_data:
#                 try:
#                     data_filtro = datetime.fromisoformat(filtro_data).date()
#                     query = query.filter(Agendamento.data_consulta == data_filtro)
#                 except:
#                     # Tentar outro formato
#                     try:
#                         data_filtro = datetime.strptime(filtro_data, '%Y-%m-%d').date()
#                         query = query.filter(Agendamento.data_consulta == data_filtro)
#                     except:
#                         pass
            
#             if filtro_medico_id:
#                 query = query.filter(Agendamento.medico_id == filtro_medico_id)
            
#             if filtro_status:
#                 query = query.filter(Agendamento.status == filtro_status)
            
#             # Ordenação
#             query = query.order_by(
#                 Agendamento.data_consulta.asc(),
#                 Agendamento.hora_consulta.asc()
#             )
            
#             # Paginação
#             total = query.count()
#             total_paginas = (total + por_pagina - 1) // por_pagina
            
#             offset = (pagina - 1) * por_pagina
#             agendamentos = query.offset(offset).limit(por_pagina).all()
            
#             return jsonify({
#                 'agendamentos': [AgendamentoController.serialize_agendamento(a) for a in agendamentos],
#                 'total': total,
#                 'pagina': pagina,
#                 'por_pagina': por_pagina,
#                 'total_paginas': total_paginas
#             }), 200
            
#         except Exception as e:
#             logger.exception("[LISTAR] Erro ao listar agendamentos")
#             return jsonify({'error': str(e)}), 500

#     # ====================
#     # OBTER AGENDAMENTO
#     # ====================
#     @staticmethod
#     def get_agendamento(id):
#         try:
#             agendamento = Agendamento.query.get(id)
#             if not agendamento:
#                 return jsonify({'message': 'Agendamento não encontrado'}), 404
            
#             return jsonify(AgendamentoController.serialize_agendamento(agendamento)), 200
            
#         except Exception as e:
#             logger.exception(f"[GET] Erro ao buscar agendamento {id}")
#             return jsonify({'error': str(e)}), 500

#     # ====================
#     # CRIAR AGENDAMENTO
#     # ====================
#     @staticmethod
#     def criar_agendamento():
#         try:
#             data = request.get_json()
            
#             # Verificar disponibilidade
#             try:
#                 data_consulta = datetime.fromisoformat(data['data_consulta']).date()
#             except:
#                 data_consulta = datetime.strptime(data['data_consulta'], '%Y-%m-%d').date()
                
#             try:
#                 hora_consulta = datetime.fromisoformat(data['hora_consulta']).time()
#             except:
#                 hora_consulta = datetime.strptime(data['hora_consulta'], '%H:%M').time()
                
#             medico_id = data['medico_id']
            
#             # Verificar se já existe agendamento no mesmo horário
#             conflito = Agendamento.query.filter(
#                 Agendamento.medico_id == medico_id,
#                 Agendamento.data_consulta == data_consulta,
#                 Agendamento.hora_consulta == hora_consulta,
#                 Agendamento.status != 'cancelado'
#             ).first()
            
#             if conflito:
#                 return jsonify({
#                     'success': False,
#                     'mensagem': 'Horário já agendado'
#                 }), 400
            
#             # Criar agendamento
#             agendamento = Agendamento(
#                 paciente_id=data.get('paciente_id'),
#                 paciente_nome=data.get('paciente_nome', 'Paciente não identificado'),
#                 telefone=data['telefone'],
#                 medico_id=medico_id,
#                 data_consulta=data_consulta,
#                 hora_consulta=hora_consulta,
#                 tipo_consulta=data.get('tipo_consulta', 'Rotina'),
#                 status=data.get('status', 'pendente'),
#                 observacoes=data.get('observacoes')
#             )
            
#             db.session.add(agendamento)
#             db.session.commit()
            
#             return jsonify({
#                 'success': True,
#                 'mensagem': 'Agendamento criado com sucesso',
#                 'id': agendamento.id
#             }), 201
            
#         except Exception as e:
#             db.session.rollback()
#             logger.exception("[CRIAR] Erro ao criar agendamento: %s", str(e))
#             return jsonify({'error': str(e), 'success': False}), 500

#     # ====================
#     # EDITAR AGENDAMENTO
#     # ====================
#     @staticmethod
#     def editar_agendamento():
#         try:
#             data = request.get_json()
#             agendamento_id = data.get('id')
            
#             if not agendamento_id:
#                 return jsonify({'success': False, 'mensagem': 'ID do agendamento é obrigatório'}), 400
            
#             agendamento = Agendamento.query.get(agendamento_id)
#             if not agendamento:
#                 return jsonify({'success': False, 'mensagem': 'Agendamento não encontrado'}), 404
            
#             # Atualizar campos
#             if 'status' in data:
#                 agendamento.status = data['status']
            
#             if 'observacoes' in data:
#                 agendamento.observacoes = data['observacoes']
            
#             # Atualizar data/hora se fornecidas
#             if 'data_consulta' in data:
#                 try:
#                     agendamento.data_consulta = datetime.fromisoformat(data['data_consulta']).date()
#                 except:
#                     agendamento.data_consulta = datetime.strptime(data['data_consulta'], '%Y-%m-%d').date()
            
#             if 'hora_consulta' in data:
#                 try:
#                     agendamento.hora_consulta = datetime.fromisoformat(data['hora_consulta']).time()
#                 except:
#                     agendamento.hora_consulta = datetime.strptime(data['hora_consulta'], '%H:%M').time()
            
#             # Se mudou para confirmado e deve enviar SMS
#             if 'enviar_sms' in data and data['enviar_sms'] and agendamento.status == 'confirmado':
#                 # Implementar envio de SMS aqui
#                 pass
            
#             db.session.commit()
            
#             return jsonify({
#                 'success': True,
#                 'mensagem': 'Agendamento atualizado com sucesso'
#             }), 200
            
#         except Exception as e:
#             db.session.rollback()
#             logger.exception("[EDITAR] Erro ao editar agendamento: %s", str(e))
#             return jsonify({'error': str(e), 'success': False}), 500

#     # ====================
#     # CANCELAR AGENDAMENTO
#     # ====================
#     @staticmethod
#     def cancelar_agendamento(id):
#         try:
#             agendamento = Agendamento.query.get(id)
#             if not agendamento:
#                 return jsonify({'success': False, 'mensagem': 'Agendamento não encontrado'}), 404
            
#             agendamento.status = 'cancelado'
#             agendamento.observacoes = (agendamento.observacoes or '') + '\n[CANCELADO pelo administrador]'
            
#             db.session.commit()
            
#             return jsonify({
#                 'success': True,
#                 'mensagem': 'Agendamento cancelado com sucesso'
#             }), 200
            
#         except Exception as e:
#             db.session.rollback()
#             logger.exception(f"[CANCELAR] Erro ao cancelar agendamento {id}: {str(e)}")
#             return jsonify({'error': str(e), 'success': False}), 500

#     # ====================
#     # LISTAR MÉDICOS
#     # ====================
#     @staticmethod
#     def listar_medicos():
#         try:
#             medicos = Medico.query.all()  # Removi filtro ativo para ver todos
#             return jsonify([AgendamentoController.serialize_medico(m) for m in medicos]), 200
            
#         except Exception as e:
#             logger.exception("[MÉDICOS] Erro ao listar médicos: %s", str(e))
#             return jsonify({'error': str(e)}), 500

#     # ====================
#     # CRIAR MÉDICO
#     # ====================
#     @staticmethod
#     def criar_medico():
#         try:
#             # Verificar se é JSON ou form-data
#             if request.is_json:
#                 data = request.get_json()
#             else:
#                 data = request.form.to_dict()
#                 # Converter string 'ativo' para booleano
#                 if 'ativo' in data:
#                     data['ativo'] = data['ativo'] == '1' or data['ativo'].lower() == 'true'
            
#             # DEBUG: Log dos dados recebidos
#             print(f"Dados recebidos para criar médico: {data}")
#             print(f"Tipo de dados: {'JSON' if request.is_json else 'FORM'}")

#             # Verificar campos obrigatórios
#             campos_obrigatorios = ['nome', 'especialidade', 'registro_profissional']
#             for campo in campos_obrigatorios:
#                 if campo not in data or not str(data[campo]).strip():
#                     return jsonify({
#                         'success': False,
#                         'mensagem': f'Campo obrigatório faltando: {campo}'
#                     }), 400
            
#             # Verificar se registro já existe
#             if 'registro_profissional' in data:
#                 exists = Medico.query.filter_by(registro_profissional=data['registro_profissional']).first()
#                 if exists:
#                     return jsonify({
#                         'success': False,
#                         'mensagem': 'Registro profissional já cadastrado'
#                     }), 400
            
#             # Processar telefone - aceitar vazio como None
#             telefone = data.get('telefone')
#             if telefone is not None:
#                 telefone = str(telefone).strip()
#                 if telefone == '':
#                     telefone = None
#                 else:
#                     # Remover espaços e caracteres não numéricos, mantendo apenas dígitos
#                     telefone = ''.join(filter(str.isdigit, telefone))
#                     # Se o telefone tiver 9 dígitos e começar com 84,85,86,87, adicionar código 258
#                     if len(telefone) == 9 and telefone[:2] in ['84', '85', '86', '87']:
#                         telefone = '258' + telefone
#                     # Se tiver menos de 9 dígitos, considerar inválido (mas não vamos bloquear, apenas avisar)
#                     elif len(telefone) < 9:
#                         print(f"Aviso: Telefone com menos de 9 dígitos: {telefone}")
            
#             print(f"Telefone processado: {telefone}")
            
#             # Criar médico
#             medico = Medico(
#                 nome=data['nome'],
#                 especialidade=data['especialidade'],
#                 registro_profissional=data.get('registro_profissional', ''),
#                 telefone=telefone,
#                 email=data.get('email'),
#                 horario_trabalho=data.get('horario_trabalho'),
#                 ativo=data.get('ativo', True)
#             )
            
#             db.session.add(medico)
#             db.session.commit()
            
#             return jsonify({
#                 'success': True,
#                 'mensagem': 'Médico criado com sucesso',
#                 'id': medico.id,
#                 'medico': AgendamentoController.serialize_medico(medico)
#             }), 201
            
#         except Exception as e:
#             db.session.rollback()
#             logger.exception("[MÉDICO CRIAR] Erro ao criar médico: %s", str(e))
#             return jsonify({'error': str(e), 'success': False}), 500

#     # ====================
#     # HORÁRIOS DO CALENDÁRIO
#     # ====================
#     @staticmethod
#     def get_calendario_horarios():
#         try:
#             # Parâmetros
#             start_str = request.args.get('start')
#             end_str = request.args.get('end')
#             medico_id = request.args.get('medico_id')
            
#             start_date = datetime.fromisoformat(start_str).date() if start_str else date.today()
#             end_date = datetime.fromisoformat(end_str).date() if end_str else start_date + timedelta(days=30)
            
#             eventos = []
            
#             # Filtro por médico
#             agendamentos_query = Agendamento.query.filter(
#                 Agendamento.data_consulta >= start_date,
#                 Agendamento.data_consulta <= end_date,
#                 Agendamento.status != 'cancelado'
#             )
            
#             if medico_id:
#                 agendamentos_query = agendamentos_query.filter(Agendamento.medico_id == medico_id)
            
#             agendamentos = agendamentos_query.all()
            
#             for ag in agendamentos:
#                 if ag.data_consulta and ag.hora_consulta:
#                     data_hora = datetime.combine(ag.data_consulta, ag.hora_consulta)
#                     eventos.append({
#                         'id': f"ag_{ag.id}",
#                         'title': f'{ag.paciente_nome} - {ag.medico.nome if ag.medico else "Médico"}',
#                         'start': data_hora.isoformat(),
#                         'end': (data_hora + timedelta(minutes=30)).isoformat(),
#                         'color': {
#                             'pendente': '#ffc107',
#                             'confirmado': '#198754',
#                             'realizado': '#0dcaf0',
#                             'cancelado': '#dc3545'
#                         }.get(ag.status, '#6c757d'),
#                         'extendedProps': {
#                             'tipo': 'agendamento',
#                             'agendamento_id': ag.id,
#                             'status': ag.status,
#                             'medico': ag.medico.nome if ag.medico else 'Médico',
#                             'paciente': ag.paciente_nome
#                         }
#                     })
            
#             # Buscar horários disponíveis dos médicos
#             horarios_query = HorarioMedico.query.filter(
#                 HorarioMedico.ativo == True
#             )
            
#             if medico_id:
#                 horarios_query = horarios_query.filter(HorarioMedico.medico_id == medico_id)
            
#             horarios = horarios_query.all()
            
#             for horario in horarios:
#                 # Determinar datas para este horário
#                 datas_aplicaveis = []
                
#                 if horario.data_especifica:
#                     # Horário específico para uma data
#                     if start_date <= horario.data_especifica <= end_date:
#                         datas_aplicaveis.append(horario.data_especifica)
#                 else:
#                     # Horário recorrente por dia da semana
#                     for dia in range((end_date - start_date).days + 1):
#                         data_atual = start_date + timedelta(days=dia)
#                         if data_atual.isoweekday() == horario.dia_semana:
#                             datas_aplicaveis.append(data_atual)
                
#                 for data_atual in datas_aplicaveis:
#                     # Criar eventos de disponibilidade
#                     hora_atual = datetime.combine(data_atual, horario.hora_inicio)
#                     hora_fim = datetime.combine(data_atual, horario.hora_fim)
                    
#                     while hora_atual < hora_fim:
#                         # Pular intervalo de almoço
#                         if (horario.intervalo_almoco_inicio and horario.intervalo_almoco_fim and
#                             horario.intervalo_almoco_inicio <= hora_atual.time() < horario.intervalo_almoco_fim):
#                             hora_atual = datetime.combine(data_atual, horario.intervalo_almoco_fim)
#                             continue
                        
#                         # Verificar se já tem agendamento neste horário
#                         agendamento_existente = Agendamento.query.filter(
#                             Agendamento.medico_id == horario.medico_id,
#                             Agendamento.data_consulta == data_atual,
#                             Agendamento.hora_consulta == hora_atual.time(),
#                             Agendamento.status != 'cancelado'
#                         ).first()
                        
#                         if not agendamento_existente:
#                             eventos.append({
#                                 'id': f'disp_{horario.id}_{hora_atual.strftime("%Y%m%d_%H%M")}',
#                                 'title': 'Disponível',
#                                 'start': hora_atual.isoformat(),
#                                 'end': (hora_atual + timedelta(minutes=horario.duracao_consulta)).isoformat(),
#                                 'color': '#d1e7dd',
#                                 'textColor': '#0f5132',
#                                 'extendedProps': {
#                                     'tipo': 'disponivel',
#                                     'medico_id': horario.medico_id,
#                                     'medico_nome': horario.medico.nome if horario.medico else 'Médico'
#                                 }
#                             })
                        
#                         hora_atual += timedelta(minutes=horario.duracao_consulta)
            
#             return jsonify(eventos), 200
            
#         except Exception as e:
#             logger.exception("[CALENDÁRIO] Erro ao buscar horários: %s", str(e))
#             return jsonify({'error': str(e)}), 500

#     # ====================
#     # SALVAR HORÁRIO
#     # ====================
#     @staticmethod
#     def salvar_horario():
#         try:
#             data = request.get_json()
            
#             medico_id = data.get('medico_id')
#             dias = data.get('dias', [])
            
#             if not medico_id or not dias:
#                 return jsonify({
#                     'success': False,
#                     'mensagem': 'Médico e dias são obrigatórios'
#                 }), 400
            
#             # Converter strings para objetos time
#             hora_inicio = datetime.strptime(data['hora_inicio'], '%H:%M').time()
#             hora_fim = datetime.strptime(data['hora_fim'], '%H:%M').time()
            
#             # Remover horários existentes para estes dias
#             HorarioMedico.query.filter(
#                 HorarioMedico.medico_id == medico_id,
#                 HorarioMedico.dia_semana.in_(dias),
#                 HorarioMedico.data_especifica == None
#             ).delete()
            
#             # Criar novos horários
#             for dia in dias:
#                 horario = HorarioMedico(
#                     medico_id=medico_id,
#                     dia_semana=int(dia),
#                     hora_inicio=hora_inicio,
#                     hora_fim=hora_fim,
#                     duracao_consulta=int(data.get('duracao', 30)),
#                     intervalo_almoco_inicio=datetime.strptime(data['almoco_inicio'], '%H:%M').time() if data.get('almoco_inicio') else None,
#                     intervalo_almoco_fim=datetime.strptime(data['almoco_fim'], '%H:%M').time() if data.get('almoco_fim') else None,
#                     ativo=True
#                 )
#                 db.session.add(horario)
            
#             db.session.commit()
            
#             return jsonify({
#                 'success': True,
#                 'mensagem': 'Horário salvo com sucesso'
#             }), 200
            
#         except Exception as e:
#             db.session.rollback()
#             logger.exception("[HORÁRIO] Erro ao salvar horário: %s", str(e))
#             return jsonify({'error': str(e), 'success': False}), 500

#     # ====================
#     # ENVIAR SMS
#     # ====================
#     @staticmethod
#     def enviar_sms():
#         try:
#             data = request.get_json()
            
#             tipo_destino = data.get('tipo_destino', 'agendamento')
#             mensagem = data.get('mensagem', '').strip()
#             tipo_sms = data.get('tipo_sms', 'personalizado')
            
#             if not mensagem:
#                 return jsonify({'success': False, 'mensagem': 'Mensagem é obrigatória'}), 400
            
#             destinatarios = []
            
#             if tipo_destino == 'telefone':
#                 telefone = data.get('telefone')
#                 if not telefone:
#                     return jsonify({'success': False, 'mensagem': 'Telefone é obrigatório'}), 400
#                 destinatarios.append({'telefone': telefone, 'nome': 'Destinatário'})
                
#             elif tipo_destino == 'agendamento':
#                 data_agendamento_str = data.get('data_agendamento')
#                 if not data_agendamento_str:
#                     return jsonify({'success': False, 'mensagem': 'Data do agendamento é obrigatória'}), 400
                
#                 try:
#                     data_agendamento = datetime.fromisoformat(data_agendamento_str).date()
#                 except:
#                     data_agendamento = datetime.strptime(data_agendamento_str, '%Y-%m-%d').date()
                    
#                 agendamentos = Agendamento.query.filter(
#                     Agendamento.data_consulta == data_agendamento,
#                     Agendamento.status.in_(['pendente', 'confirmado'])
#                 ).all()
                
#                 for ag in agendamentos:
#                     destinatarios.append({
#                         'telefone': ag.telefone,
#                         'nome': ag.paciente_nome,
#                         'agendamento_id': ag.id
#                     })
                    
#             elif tipo_destino == 'todos':
#                 pacientes = Observation.query.filter(Observation.contact.isnot(None)).all()
#                 for p in pacientes:
#                     if p.contact:
#                         destinatarios.append({
#                             'telefone': p.contact,
#                             'nome': p.fullname,
#                             'paciente_id': p.id
#                         })
            
#             # Enviar SMS para cada destinatário
#             sms_ids = []
#             for dest in destinatarios:
#                 sms = SMS(
#                     destinatario=dest['telefone'],
#                     destinatario_nome=dest.get('nome'),
#                     mensagem=mensagem,
#                     tipo=tipo_sms,
#                     agendamento_id=dest.get('agendamento_id'),
#                     status='pendente'  # Mudar para 'enviado' quando integrar com provedor
#                 )
                
#                 db.session.add(sms)
#                 db.session.flush()  # Para obter o ID
#                 sms_ids.append(sms.id)
            
#             db.session.commit()
            
#             # SIMULAÇÃO - Em produção, integrar com provedor SMS aqui
#             # for sms_id in sms_ids:
#             #     sms = SMS.query.get(sms_id)
#             #     resultado = enviar_para_provedor_sms(sms.destinatario, sms.mensagem)
#             #     sms.status = 'enviado' if resultado.success else 'falha'
#             #     sms.mensagem_id = resultado.message_id
#             #     sms.resposta = resultado.response
            
#             return jsonify({
#                 'success': True,
#                 'mensagem': f'SMS programado para {len(destinatarios)} destinatários',
#                 'total': len(destinatarios),
#                 'sms_ids': sms_ids
#             }), 200
            
#         except Exception as e:
#             db.session.rollback()
#             logger.exception("[SMS] Erro ao enviar SMS: %s", str(e))
#             return jsonify({'error': str(e), 'success': False}), 500

#     # ====================
#     # HISTÓRICO DE SMS
#     # ====================
#     @staticmethod
#     def historico_sms():
#         try:
#             sms_list = SMS.query.order_by(SMS.data_envio.desc()).limit(50).all()
#             return jsonify({
#                 'historico': [AgendamentoController.serialize_sms(s) for s in sms_list]
#             }), 200
            
#         except Exception as e:
#             logger.exception("[HISTÓRICO SMS] Erro ao buscar histórico: %s", str(e))
#             return jsonify({'error': str(e)}), 500

#     # ====================
#     # LISTAR PACIENTES (para select)
#     # ====================
#     @staticmethod
#     def listar_pacientes():
#         try:
#             pacientes = Observation.query.filter(
#                 Observation.contact.isnot(None),
#                 Observation.contact != ''
#             ).order_by(Observation.fullname).limit(100).all()
            
#             pacientes_data = []
#             for p in pacientes:
#                 pacientes_data.append({
#                     'id': p.id,
#                     'nid': p.nid,
#                     'fullname': p.fullname,
#                     'contact': p.contact,
#                     'age': p.age,
#                     'gender': p.gender
#                 })
            
#             return jsonify(pacientes_data), 200
            
#         except Exception as e:
#             logger.exception("[PACIENTES] Erro ao listar pacientes: %s", str(e))
#             return jsonify({'error': str(e)}), 500

#     # ====================
#     # ATUALIZAR HORÁRIO DO AGENDAMENTO (drag & drop)
#     # ====================
#     @staticmethod
#     def atualizar_horario_agendamento():
#         try:
#             data = request.get_json()
#             agendamento_id = data.get('agendamento_id')
#             nova_data_hora = data.get('nova_data_hora')
            
#             if not agendamento_id or not nova_data_hora:
#                 return jsonify({'success': False, 'mensagem': 'Dados incompletos'}), 400
            
#             agendamento = Agendamento.query.get(agendamento_id)
#             if not agendamento:
#                 return jsonify({'success': False, 'mensagem': 'Agendamento não encontrado'}), 404
            
#             # Converter nova data/hora
#             nova_data_hora_dt = datetime.fromisoformat(nova_data_hora.replace('Z', '+00:00'))
#             nova_data = nova_data_hora_dt.date()
#             nova_hora = nova_data_hora_dt.time()
            
#             # Verificar conflito
#             conflito = Agendamento.query.filter(
#                 Agendamento.id != agendamento_id,
#                 Agendamento.medico_id == agendamento.medico_id,
#                 Agendamento.data_consulta == nova_data,
#                 Agendamento.hora_consulta == nova_hora,
#                 Agendamento.status != 'cancelado'
#             ).first()
            
#             if conflito:
#                 return jsonify({
#                     'success': False,
#                     'mensagem': 'Horário já ocupado'
#                 }), 400
            
#             # Atualizar
#             agendamento.data_consulta = nova_data
#             agendamento.hora_consulta = nova_hora
            
#             db.session.commit()
            
#             return jsonify({
#                 'success': True,
#                 'mensagem': 'Horário atualizado com sucesso'
#             }), 200
            
#         except Exception as e:
#             db.session.rollback()
#             logger.exception("[ATUALIZAR HORÁRIO] Erro: %s", str(e))
#             return jsonify({'error': str(e), 'success': False}), 500
        
#     # @staticmethod
#     # def historico_sms():
#     #     try:
#     #         logger.info("[HISTÓRICO SMS] Método chamado")
#     #         sms_list = SMS.query.order_by(SMS.data_envio.desc()).limit(50).all()
#     #         logger.info(f"[HISTÓRICO SMS] Encontrados {len(sms_list)} registros")
#     #         return jsonify({
#     #             'historico': [AgendamentoController.serialize_sms(s) for s in sms_list]
#     #         }), 200
            
#     #     except Exception as e:
#     #         logger.exception("[HISTÓRICO SMS] Erro ao buscar histórico: %s", str(e))
#     #         return jsonify({'error': str(e)}), 500