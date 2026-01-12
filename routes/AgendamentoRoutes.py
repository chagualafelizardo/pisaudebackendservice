import re
from flask import Blueprint, render_template, jsonify, request
from controllers.AgendamentoController import AgendamentoController
from models import Medico, Observation, Agendamento,HorarioMedico, db
from datetime import date, datetime, timedelta
import logging
from datetime import datetime, date, timedelta, time

logger = logging.getLogger(__name__)

agendamento_bp = Blueprint('agendamento', __name__)

# ====================
# PÁGINAS HTML
# ====================

@agendamento_bp.route('/agendamentos')
def admin_agendamentos():
    # Buscar médicos ATIVOS para o modal
    medicos = Medico.query.filter_by(ativo=True).order_by(Medico.nome).all()
    
    return render_template('admin/agendamentos.html',
                         hoje=date.today().isoformat(),
                         medicos=medicos)

# ====================
# API - AGENDAMENTOS
# ====================

@agendamento_bp.route('/agendamentos/estatisticas', methods=['GET'])
def get_estatisticas():
    return AgendamentoController.get_estatisticas()

@agendamento_bp.route('/agendamentos/listar', methods=['GET', 'POST'])
def listar_agendamentos():
    return AgendamentoController.listar_agendamentos()

@agendamento_bp.route('/agendamentos/<int:id>', methods=['GET'])
def get_agendamento(id):
    return AgendamentoController.get_agendamento(id)

@agendamento_bp.route('/agendamentos/criar', methods=['POST'])
def criar_agendamento():
    return AgendamentoController.criar_agendamento()

@agendamento_bp.route('/agendamentos/editar', methods=['POST'])
def editar_agendamento():
    return AgendamentoController.editar_agendamento()

@agendamento_bp.route('/agendamentos/cancelar/<int:id>', methods=['POST'])
def cancelar_agendamento(id):
    return AgendamentoController.cancelar_agendamento(id)

@agendamento_bp.route('/agendamentos/atualizar-horario', methods=['POST'])
def atualizar_horario_agendamento():
    return AgendamentoController.atualizar_horario_agendamento()

@agendamento_bp.route('/agendamentos/horarios/medico/<int:medico_id>', methods=['GET'])
def get_horarios_medico(medico_id):
    return AgendamentoController.get_horarios_medico(medico_id)

# ====================
# API - MÉDICOS (ROTAS COMPLETAS)
# ====================

@agendamento_bp.route('/agendamentos/medicos', methods=['GET', 'POST'])
def medicos():
    if request.method == 'GET':
        return AgendamentoController.listar_medicos()
    elif request.method == 'POST':
        return AgendamentoController.criar_medico()

# Esta função foi movida para cima (removida daqui para evitar duplicação)
# @agendamento_bp.route('/agendamentos')
# def admin_agendamentos():
#     # Buscar médicos ATIVOS para o modal
#     medicos = Medico.query.filter_by(ativo=True).order_by(Medico.nome).all()
#    
#     return render_template('admin/agendamentos.html',
#                          hoje=date.today().isoformat(),
#                          medicos=medicos)

@agendamento_bp.route('/agendamentos/horarios/disponiveis', methods=['GET'])
def horarios_disponiveis():
    try:
        medico_id = request.args.get('medico_id')
        data_str = request.args.get('data')
        
        if not medico_id or not data_str:
            return jsonify({'disponiveis': [], 'mensagem': 'Parâmetros incompletos'}), 400
        
        # Converter data
        try:
            data_consulta = datetime.fromisoformat(data_str).date()
        except:
            data_consulta = datetime.strptime(data_str, '%Y-%m-%d').date()
        
        # Buscar horários do médico nesse dia da semana
        dia_semana = data_consulta.isoweekday()
        horarios = HorarioMedico.query.filter_by(
            medico_id=medico_id,
            dia_semana=dia_semana,
            ativo=True
        ).all()
        
        disponiveis = []
        
        for horario in horarios:
            # Gerar slots de horários disponíveis
            hora_atual = datetime.combine(data_consulta, horario.hora_inicio)
            hora_fim = datetime.combine(data_consulta, horario.hora_fim)
            
            while hora_atual < hora_fim:
                # Pular intervalo de almoço
                if (horario.intervalo_almoco_inicio and horario.intervalo_almoco_fim and
                    horario.intervalo_almoco_inicio <= hora_atual.time() < horario.intervalo_almoco_fim):
                    hora_atual = datetime.combine(data_consulta, horario.intervalo_almoco_fim)
                    continue
                
                # Verificar se já tem agendamento
                agendamento_existente = Agendamento.query.filter(
                    Agendamento.medico_id == medico_id,
                    Agendamento.data_consulta == data_consulta,
                    Agendamento.hora_consulta == hora_atual.time(),
                    Agendamento.status != 'cancelado'
                ).first()
                
                if not agendamento_existente:
                    disponiveis.append({
                        'hora': hora_atual.strftime('%H:%M'),
                        'disponivel': True
                    })
                
                hora_atual += timedelta(minutes=horario.duracao_consulta)
        
        return jsonify({
            'disponiveis': disponiveis,
            'medico_id': medico_id,
            'data': data_str
        }), 200
        
    except Exception as e:
        logger.exception("[HORARIOS DISPONIVEIS] Erro: %s", str(e))
        return jsonify({'error': str(e)}), 500
    
# Rota para listar horários dos médicos (todos ou filtrado por médico)
@agendamento_bp.route('/agendamentos/medicos/horarios', methods=['GET'])
def get_all_horarios():
    try:
        medico_id = request.args.get('medico_id')
        dia_semana = request.args.get('dia_semana')
        
        query = HorarioMedico.query.filter_by(ativo=True)
        
        if medico_id:
            query = query.filter_by(medico_id=medico_id)
        
        if dia_semana:
            query = query.filter_by(dia_semana=dia_semana)
        
        horarios = query.all()
        
        # Usar o método serialize_horario do Controller
        return jsonify({
            'success': True,
            'horarios': [AgendamentoController.serialize_horario(h) for h in horarios]
        }), 200
        
    except Exception as e:
        logger.exception(f"[ALL HORARIOS] Erro: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
# No arquivo routes.py
@agendamento_bp.route('/agendamentos/horarios/todos', methods=['GET'])
def get_todos_horarios():
    try:
        horarios = HorarioMedico.query.all()
        return jsonify({
            'success': True,
            'horarios': [AgendamentoController.serialize_horario(h) for h in horarios]
        }), 200
    except Exception as e:
        logger.exception(f"[TODOS HORARIOS] Erro: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
# Rota para obter médico específico
@agendamento_bp.route('/agendamentos/medicos/<int:id>', methods=['GET'])
def get_medico(id):
    try:
        print(f"=== GET MÉDICO ID: {id} ===")
        medico = Medico.query.get(id)
        
        if not medico:
            print(f"Médico {id} não encontrado")
            return jsonify({'success': False, 'mensagem': 'Médico não encontrado'}), 404
        
        print(f"Médico encontrado: {medico.nome}")
        
        return jsonify({
            'success': True,
            'medico': {
                'id': medico.id,
                'nome': medico.nome,
                'especialidade': medico.especialidade,
                'registro_profissional': medico.registro_profissional,
                'telefone': medico.telefone,
                'email': medico.email,
                'horario_trabalho': medico.horario_trabalho,
                'ativo': medico.ativo
            }
        }), 200
    except Exception as e:
        print(f"ERRO: {str(e)}")
        logger.exception("Erro ao obter médico: %s", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500

# Rota para atualizar médico
@agendamento_bp.route('/agendamentos/medicos/<int:id>', methods=['PUT'])
def update_medico(id):
    try:
        print(f"=== ATUALIZAR MÉDICO ID: {id} ===")
        medico = Medico.query.get(id)
        
        if not medico:
            print(f"Médico {id} não encontrado")
            return jsonify({'success': False, 'mensagem': 'Médico não encontrado'}), 404
        
        data = request.get_json()
        print(f"Dados recebidos: {data}")
        
        # Atualizar campos
        if 'nome' in data:
            medico.nome = data['nome'].strip()
        if 'especialidade' in data:
            medico.especialidade = data['especialidade'].strip()
        if 'registro_profissional' in data:
            medico.registro_profissional = data['registro_profissional'].strip()
        if 'telefone' in data:
            medico.telefone = data['telefone'] if data['telefone'] else None
        if 'email' in data:
            medico.email = data['email'].strip() if data['email'] else None
        if 'horario_trabalho' in data:
            medico.horario_trabalho = data['horario_trabalho'].strip() if data['horario_trabalho'] else None
        if 'ativo' in data:
            medico.ativo = bool(data['ativo'])
        
        db.session.commit()
        print(f"Médico {id} atualizado com sucesso")
        
        return jsonify({
            'success': True,
            'mensagem': 'Médico atualizado com sucesso',
            'medico': {
                'id': medico.id,
                'nome': medico.nome,
                'especialidade': medico.especialidade,
                'telefone': medico.telefone,
                'email': medico.email,
                'horario_trabalho': medico.horario_trabalho,
                'ativo': medico.ativo
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"ERRO ao atualizar médico: {str(e)}")
        logger.exception("Erro ao atualizar médico: %s", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500

# Rota para excluir médico
@agendamento_bp.route('/agendamentos/medicos/<int:id>', methods=['DELETE'])
def delete_medico(id):
    try:
        print(f"=== EXCLUIR MÉDICO ID: {id} ===")
        medico = Medico.query.get(id)
        
        if not medico:
            print(f"Médico {id} não encontrado")
            return jsonify({'success': False, 'mensagem': 'Médico não encontrado'}), 404
        
        # Verificar se o médico tem agendamentos futuros
        agendamentos_futuros = Agendamento.query.filter(
            Agendamento.medico_id == id,
            Agendamento.data_consulta >= datetime.now().date(),
            Agendamento.status.in_(['pendente', 'confirmado'])
        ).count()
        
        print(f"Agendamentos futuros encontrados: {agendamentos_futuros}")
        
        if agendamentos_futuros > 0:
            return jsonify({
                'success': False,
                'mensagem': f'Não é possível excluir o médico. Existem {agendamentos_futuros} agendamentos futuros.'
            }), 400
        
        # Excluir médico
        db.session.delete(medico)
        db.session.commit()
        
        print(f"Médico {id} excluído com sucesso")
        
        return jsonify({
            'success': True,
            'mensagem': 'Médico excluído com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"ERRO ao excluir médico: {str(e)}")
        logger.exception("Erro ao excluir médico: %s", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500

# ====================
# API - HORÁRIOS
# ====================

@agendamento_bp.route('/agendamentos/horarios/calendario', methods=['GET'])
def get_calendario_horarios():
    return AgendamentoController.get_calendario_horarios()

@agendamento_bp.route('/agendamentos/horarios/salvar', methods=['POST'])
def salvar_horario():
    return AgendamentoController.salvar_horario()

# ====================
# API - SMS
# ====================

@agendamento_bp.route('/agendamentos/sms/enviar', methods=['POST'])
def enviar_sms():
    return AgendamentoController.enviar_sms()

@agendamento_bp.route('/agendamentos/sms/historico', methods=['GET'])
def historico_sms():
    return AgendamentoController.historico_sms()

# ====================
# API - PACIENTES
# ====================

@agendamento_bp.route('/agendamentos/pacientes', methods=['GET'])
def listar_pacientes():
    return AgendamentoController.listar_pacientes()

# ====================
# ROTAS PARA PACIENTES (público)
# ====================

@agendamento_bp.route('/agendamentos/disponiveis', methods=['GET'])
def horarios_disponiveis_publico():  # Renomeada para evitar conflito
    medico_id = request.args.get('medico_id')
    data = request.args.get('data')
    
    # Implementar lógica de disponibilidade
    return jsonify({'disponiveis': [], 'medico_id': medico_id, 'data': data}), 200

@agendamento_bp.route('/agendamentos/criar-publico', methods=['POST'])
def criar_agendamento_paciente():
    return AgendamentoController.criar_agendamento()

# ====================
# ROTAS AUXILIARES
# ====================

# Rota para verificar se registro profissional já existe
@agendamento_bp.route('/agendamentos/medicos/verificar-registro', methods=['POST'])
def verificar_registro():
    try:
        data = request.get_json()
        registro = data.get('registro_profissional')
        
        if not registro:
            return jsonify({'exists': False}), 200
        
        medico = Medico.query.filter_by(registro_profissional=registro).first()
        
        if medico:
            return jsonify({
                'exists': True,
                'medico': {
                    'id': medico.id,
                    'nome': medico.nome,
                    'especialidade': medico.especialidade
                }
            }), 200
        else:
            return jsonify({'exists': False}), 200
            
    except Exception as e:
        logger.exception("Erro ao verificar registro: %s", str(e))
        return jsonify({'error': str(e)}), 500

# Rota para listar médicos ativos (para selects)
@agendamento_bp.route('/agendamentos/medicos/ativos', methods=['GET'])
def medicos_ativos():
    try:
        medicos = Medico.query.filter_by(ativo=True).order_by(Medico.nome).all()
        medicos_list = []
        
        for medico in medicos:
            medicos_list.append({
                'id': medico.id,
                'nome': medico.nome,
                'especialidade': medico.especialidade,
                'telefone': medico.telefone
            })
        
        return jsonify(medicos_list), 200
        
    except Exception as e:
        logger.exception("Erro ao listar médicos ativos: %s", str(e))
        return jsonify({'error': str(e)}), 500

# Rota para alterar status do médico (ativar/desativar)
@agendamento_bp.route('/agendamentos/medicos/<int:id>/status', methods=['PATCH'])
def alterar_status_medico(id):
    try:
        data = request.get_json()
        medico = Medico.query.get(id)
        
        if not medico:
            return jsonify({'success': False, 'mensagem': 'Médico não encontrado'}), 404
        
        if 'ativo' in data:
            medico.ativo = bool(data['ativo'])
            db.session.commit()
            
            status = 'ativado' if medico.ativo else 'desativado'
            return jsonify({
                'success': True,
                'mensagem': f'Médico {status} com sucesso'
            }), 200
        else:
            return jsonify({'success': False, 'mensagem': 'Campo "ativo" não fornecido'}), 400
            
    except Exception as e:
        db.session.rollback()
        logger.exception("Erro ao alterar status do médico: %s", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500
    

# Agendamento apartir do Smartphone
@agendamento_bp.route('/appointments/process-sms', methods=['POST'])
def process_sms_appointment():
    try:
        data = request.get_json()
        phone = data.get('phone')
        original_message = data.get('message', '').strip()
        
        logger.info(f"[SMS AGENDAMENTO] Recebido de {phone}: {original_message}")
        
        # Normalizar a mensagem: converter para minúsculas e remover espaços extras
        message = ' '.join(original_message.lower().split())
        logger.info(f"[SMS AGENDAMENTO] Mensagem normalizada: '{message}'")
        
        # Padrão completo para mensagem com NID
        # consulta 0110000001/2015/00396 12/01/2026 08:00
        pattern_with_nid = r'^(consulta|agendar|marcar)\s+(\d{10}/\d{4}/\d{5})\s+(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s+(\d{1,2})[:.](\d{2})$'
        
        # Padrão para mensagem sem NID
        # consulta 12/01/2026 08:00
        pattern_without_nid = r'^(consulta|agendar|marcar)\s+(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s+(\d{1,2})[:.](\d{2})$'
        
        # Primeiro tentar com NID
        match = re.match(pattern_with_nid, message)
        has_nid = True
        
        if not match:
            # Tentar sem NID
            match = re.match(pattern_without_nid, message)
            has_nid = False
        
        if not match:
            logger.warning(f"[SMS AGENDAMENTO] Padrão não encontrado. Mensagem: '{message}'")
            return jsonify({
                'success': False,
                'mensagem': 'Formato inválido. Use: consulta NID DD/MM/AAAA HH:MM (ex: consulta 0110000001/2015/00396 12/01/2026 08:00) ou consulta DD/MM/AAAA HH:MM'
            }), 400
        
        groups = match.groups()
        logger.info(f"[SMS AGENDAMENTO] Grupos capturados: {groups}")
        
        if has_nid:
            nid = groups[1]  # Já está no formato string
            dia, mes, ano, hora, minuto = groups[2:]
        else:
            nid = None
            dia, mes, ano, hora, minuto = groups[1:]
        
        # Formatar data no padrão YYYY-MM-DD
        data_consulta = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
        
        # Formatar hora no padrão HH:MM
        hora_consulta = f"{hora.zfill(2)}:{minuto.zfill(2)}"
        
        logger.info(f"[SMS AGENDAMENTO] NID: {nid}, Data: {data_consulta}, Hora: {hora_consulta}")
        
        # Buscar médico ativo
        medico = Medico.query.filter_by(ativo=True).first()
        
        if not medico:
            return jsonify({
                'success': False,
                'mensagem': 'Nenhum médico disponível no momento'
            }), 400
        
        # Verificar conflito de horário
        data_consulta_obj = datetime.strptime(data_consulta, '%Y-%m-%d').date()
        hora_consulta_obj = datetime.strptime(hora_consulta, '%H:%M').time()
        
        conflito = Agendamento.query.filter(
            Agendamento.medico_id == medico.id,
            Agendamento.data_consulta == data_consulta_obj,
            Agendamento.hora_consulta == hora_consulta_obj,
            Agendamento.status != 'cancelado'
        ).first()
        
        if conflito:
            logger.warning(f"[SMS AGENDAMENTO] Horário já ocupado: {data_consulta} {hora_consulta}")
            return jsonify({
                'success': False,
                'mensagem': 'Horário já agendado. Por favor, escolha outro horário.'
            }), 400
        
        # Determinar nome do paciente baseado no NID
        if nid:
            # Usar NID no nome do paciente
            paciente_nome = f"Paciente NID: {nid}"
        else:
            # Usar telefone para identificar
            paciente_nome = f"Paciente SMS: {phone}"
        
        # Criar agendamento - NÃO buscamos no banco, apenas criamos
        agendamento = Agendamento(
            paciente_id=None,  # Não associamos a um paciente existente
            paciente_nome=paciente_nome,
            telefone=phone,
            medico_id=medico.id,
            data_consulta=data_consulta_obj,
            hora_consulta=hora_consulta_obj,
            tipo_consulta='Consulta via SMS',
            status='pendente',
            observacoes=f"NID: {nid if nid else 'Não informado'}. Agendado via SMS: {original_message}",
            createAt=datetime.now()
        )
        
        db.session.add(agendamento)
        db.session.commit()
        
        logger.info(f"[SMS AGENDAMENTO] Agendamento criado com sucesso: ID {agendamento.id}")
        
        return jsonify({
            'success': True,
            'mensagem': 'Agendamento criado com sucesso',
            'appointment': {
                'id': agendamento.id,
                'patient_id': None,  # Não temos paciente_id
                'patient_name': paciente_nome,
                'telefone': phone,
                'data_consulta': data_consulta,
                'hora_consulta': hora_consulta,
                'medico_id': medico.id,
                'medico_nome': medico.nome,
                'tipo_consulta': 'Consulta via SMS',
                'status': 'pendente',
                'observacoes': f"NID: {nid if nid else 'Não informado'}. Agendado via SMS",
                'nid': nid
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.exception(f"[SMS AGENDAMENTO] Erro: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
        

@agendamento_bp.route('/appointments/available-doctors', methods=['GET'])
def get_available_doctors():
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({'success': False, 'error': 'Data é obrigatória'}), 400
        
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Buscar todos os médicos
        medicos = Medico.query.filter_by(ativo=True).all()
        
        available_doctors = []
        
        for medico in medicos:
            # Verificar horários do médico
            horarios = HorarioMedico.query.filter_by(
                medico_id=medico.id
            ).all()
            
            # Verificar se já tem agendamentos na data
            agendamentos_count = Agendamento.query.filter_by(
                medico_id=medico.id,
                data_consulta=target_date,
                status='confirmado'
            ).count()
            
            # Calcular disponibilidade
            disponibilidade = "Disponível"
            if agendamentos_count > 5:  # Exemplo: limite de 5 consultas por dia
                disponibilidade = "Limitado"
            if agendamentos_count > 8:
                disponibilidade = "Indisponível"
            
            available_doctors.append({
                'id': medico.id,
                'name': medico.nome,
                'specialty': medico.especialidade,
                'availability': disponibilidade
            })
        
        return jsonify({
            'success': True,
            'doctors': available_doctors
        }), 200
        
    except Exception as e:
        logger.exception(f"[DOCTORES DISPONÍVEIS] Erro: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500