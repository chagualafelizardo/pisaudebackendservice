from flask import jsonify, request
from datetime import datetime
from models import db, Observation, State, Textmessage, Grouptype, Group, Location, User

class ObservationController:
    @staticmethod
    def get_all():
        try:
            query = Observation.query

            # 🔥 Filtros opcionais do frontend
            textId = request.args.get('textmessageId')
            stateId = request.args.get('stateId')
            groupId = request.args.get('groupId')
            groupTypeId = request.args.get('grouptypeId')
            locationId = request.args.get('locationId')
            
            # 🔥 NOVOS FILTROS POR DATA DE ENVIO
            startDate = request.args.get('startDate')
            endDate = request.args.get('endDate')

            if textId:
                query = query.filter(Observation.textmessageId == int(textId))

            if stateId:
                query = query.filter(Observation.stateId == int(stateId))

            if groupId:
                if groupId == '0' or groupId == 'no_group':
                    # Filtro para observações SEM grupo
                    query = query.filter(Observation.groupId.is_(None))
                else:
                    query = query.filter(Observation.groupId == int(groupId))

            if groupTypeId:
                query = query.filter(Observation.grouptypeId == int(groupTypeId))

            if locationId:
                query = query.filter(Observation.locationId == int(locationId))
            
            # 🔥 FILTROS POR DATA DE ENVIO (dataenvio) - CORRIGIDO
            if startDate:
                try:
                    # Formato: YYYY-MM-DD
                    from datetime import datetime
                    start_date = datetime.strptime(startDate, '%Y-%m-%d')
                    query = query.filter(Observation.dataenvio >= start_date)
                    print(f"Filtrando por startDate: {startDate} -> {start_date}")
                except Exception as e:
                    print(f"Erro ao converter startDate {startDate}: {e}")
                    # Tenta outro formato
                    try:
                        start_date = datetime.fromisoformat(startDate.replace('Z', '+00:00'))
                        query = query.filter(Observation.dataenvio >= start_date)
                    except Exception as e2:
                        print(f"Erro ao converter startDate (formato ISO): {e2}")
            
            if endDate:
                try:
                    # Formato: YYYY-MM-DD
                    from datetime import datetime, timedelta
                    end_date = datetime.strptime(endDate, '%Y-%m-%d')
                    # Adiciona 23:59:59.999 ao final do dia
                    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                    query = query.filter(Observation.dataenvio <= end_date)
                    print(f"Filtrando por endDate: {endDate} -> {end_date}")
                except Exception as e:
                    print(f"Erro ao converter endDate {endDate}: {e}")
                    # Tenta outro formato
                    try:
                        end_date = datetime.fromisoformat(endDate.replace('Z', '+00:00'))
                        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                        query = query.filter(Observation.dataenvio <= end_date)
                    except Exception as e2:
                        print(f"Erro ao converter endDate (formato ISO): {e2}")

            observations = query.all()
            print(f"Total de observações encontradas após filtros: {len(observations)}")

            result = []
            for obs in observations:
                # Informações do grupo - usando a estrutura que já estava funcionando
                group_info = None
                if obs.group:
                    group_info = {
                        'id': obs.group.id,
                        'description': obs.group.description,
                        # Nota: Se Group não tiver relação direta com Grouptype,
                        # usamos o grouptypeId da Observation
                        'grouptypeId': obs.grouptypeId,
                        'grouptypeDescription': obs.grouptype.description if obs.grouptype else None
                    }
                
                result.append({
                    'id': obs.id,
                    'nid': obs.nid,
                    'fullname': obs.fullname,
                    'gender': obs.gender,
                    'age': obs.age,
                    'contact': obs.contact,
                    'occupation': obs.occupation,
                    'datainiciotarv': obs.datainiciotarv.isoformat() if obs.datainiciotarv else None,
                    'datalevantamento': obs.datalevantamento.isoformat() if obs.datalevantamento else None,
                    'dataproximolevantamento': obs.dataproximolevantamento.isoformat() if obs.dataproximolevantamento else None,
                    'dataconsulta': obs.dataconsulta.isoformat() if obs.dataconsulta else None,
                    'dataproximaconsulta': obs.dataproximaconsulta.isoformat() if obs.dataproximaconsulta else None,
                    'dataalocacao': obs.dataalocacao.isoformat() if obs.dataalocacao else None,
                    'dataenvio': obs.dataenvio.isoformat() if obs.dataenvio else None,
                    'dataprimeiracv': obs.dataprimeiracv.isoformat() if obs.dataprimeiracv else None,
                    'valorprimeiracv': obs.valorprimeiracv,
                    'dataultimacv': obs.dataultimacv.isoformat() if obs.dataultimacv else None,
                    'valorultimacv': obs.valorultimacv,
                    'linhaterapeutica': obs.linhaterapeutica,
                    'regime': obs.regime,
                    'status': obs.status,
                    'smsStatus': obs.smsStatus,

                    # 🔥 IDs
                    'stateId': obs.stateId,
                    'textmessageId': obs.textmessageId,
                    'grouptypeId': obs.grouptypeId,
                    'groupId': obs.groupId,
                    'locationId': obs.locationId,
                    'userId': obs.userId,

                    # 🔥 Descrições completas
                    'stateDescription': obs.state.description if obs.state else None,
                    'textMessageDescription': obs.textmessage.messagetext if obs.textmessage else None,
                    'groupTypeDescription': obs.grouptype.description if obs.grouptype else None,
                    'groupDescription': obs.group.description if obs.group else None,
                    'locationName': obs.location.name if obs.location else None,
                    'userFullName': obs.user.fullname if obs.user else None,
                    
                    # 🔥 Informações detalhadas do grupo
                    'group': group_info,

                    'createAt': obs.createAt.isoformat() if obs.createAt else None,
                    'updateAt': obs.updateAt.isoformat() if obs.updateAt else None
                })

            return jsonify(result), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @staticmethod
    def get_filtered():
        """Endpoint específico para filtragem avançada do dashboard - FILTRO POR dataenvio"""
        try:
            query = Observation.query

            # Parâmetros de filtro
            state_id = request.args.get('stateId')
            group_id = request.args.get('groupId')
            location_id = request.args.get('locationId')
            start_date_str = request.args.get('startDate')
            end_date_str = request.args.get('endDate')

            print(f"📋 Filtros recebidos: stateId={state_id}, groupId={group_id}, "
                f"locationId={location_id}, startDate={start_date_str}, endDate={end_date_str}")

            # Aplicar filtros
            if state_id and state_id != '' and state_id != 'null':
                query = query.filter(Observation.stateId == int(state_id))
                print(f"✅ Filtro stateId aplicado: {state_id}")

            if group_id and group_id != '' and group_id != 'null':
                if group_id == 'no_group':
                    query = query.filter(Observation.groupId.is_(None))
                    print(f"✅ Filtro grupo aplicado: SEM GRUPO")
                else:
                    query = query.filter(Observation.groupId == int(group_id))
                    print(f"✅ Filtro grupo aplicado: {group_id}")

            if location_id and location_id != '' and location_id != 'null':
                query = query.filter(Observation.locationId == int(location_id))
                print(f"✅ Filtro localização aplicado: {location_id}")

            # Filtro por dataenvio (data de envio) - CORRIGIDO
            from datetime import datetime
            
            if start_date_str and start_date_str != '' and start_date_str != 'null':
                try:
                    # Converter string para datetime (formato: YYYY-MM-DD)
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                    print(f"📅 Filtro dataenvio - INÍCIO: {start_date}")
                    
                    # Filtrar onde dataenvio é >= data_inicio
                    # IMPORTANTE: Observações sem dataenvio não serão incluídas
                    query = query.filter(Observation.dataenvio >= start_date)
                    
                except Exception as e:
                    print(f"❌ Erro ao processar startDate {start_date_str}: {e}")

            if end_date_str and end_date_str != '' and end_date_str != 'null':
                try:
                    # Converter string para datetime (formato: YYYY-MM-DD)
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                    # Ajustar para fim do dia (23:59:59.999)
                    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                    print(f"📅 Filtro dataenvio - FIM: {end_date}")
                    
                    # Filtrar onde dataenvio é <= data_fim
                    query = query.filter(Observation.dataenvio <= end_date)
                    
                except Exception as e:
                    print(f"❌ Erro ao processar endDate {end_date_str}: {e}")

            # Se ambas as datas foram fornecidas, podemos fazer verificação adicional
            if start_date_str and end_date_str:
                print(f"📊 Filtro por INTERVALO de dataenvio: {start_date_str} a {end_date_str}")
            
            # Executar query
            observations = query.order_by(Observation.dataenvio.desc()).all()
            print(f"✅ Total de observações filtradas: {len(observations)}")
            
            # Para debug: mostrar algumas datas
            for i, obs in enumerate(observations[:3]):
                print(f"  Obs {i+1}: id={obs.id}, dataenvio={obs.dataenvio}, estado={obs.state.description if obs.state else 'N/A'}")

            # Serializar resultados
            result = []
            for obs in observations:
                result.append({
                    'id': obs.id,
                    'nid': obs.nid,
                    'fullname': obs.fullname,
                    'gender': obs.gender,
                    'age': obs.age,
                    'contact': obs.contact,
                    'occupation': obs.occupation,
                    'datainiciotarv': obs.datainiciotarv.isoformat() if obs.datainiciotarv else None,
                    'datalevantamento': obs.datalevantamento.isoformat() if obs.datalevantamento else None,
                    'dataproximolevantamento': obs.dataproximolevantamento.isoformat() if obs.dataproximolevantamento else None,
                    'dataconsulta': obs.dataconsulta.isoformat() if obs.dataconsulta else None,
                    'dataproximaconsulta': obs.dataproximaconsulta.isoformat() if obs.dataproximaconsulta else None,
                    'dataalocacao': obs.dataalocacao.isoformat() if obs.dataalocacao else None,
                    'dataenvio': obs.dataenvio.isoformat() if obs.dataenvio else None,
                    'dataprimeiracv': obs.dataprimeiracv.isoformat() if obs.dataprimeiracv else None,
                    'valorprimeiracv': obs.valorprimeiracv,
                    'dataultimacv': obs.dataultimacv.isoformat() if obs.dataultimacv else None,
                    'valorultimacv': obs.valorultimacv,
                    'linhaterapeutica': obs.linhaterapeutica,
                    'regime': obs.regime,
                    'status': obs.status,
                    'smsStatus': obs.smsStatus,
                    
                    'stateId': obs.stateId,
                    'textmessageId': obs.textmessageId,
                    'grouptypeId': obs.grouptypeId,
                    'groupId': obs.groupId,
                    'locationId': obs.locationId,
                    'userId': obs.userId,
                    
                    'stateDescription': obs.state.description if obs.state else None,
                    'textMessageDescription': obs.textmessage.messagetext if obs.textmessage else None,
                    'groupTypeDescription': obs.grouptype.description if obs.grouptype else None,
                    'groupDescription': obs.group.description if obs.group else None,
                    'locationName': obs.location.name if obs.location else None,
                    'userFullName': obs.user.fullname if obs.user else None,
                    
                    'createAt': obs.createAt.isoformat() if obs.createAt else None,
                    'updateAt': obs.updateAt.isoformat() if obs.updateAt else None
                })

            return jsonify(result), 200

        except Exception as e:
            print(f"❌ ERRO CRÍTICO no endpoint filtrado: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
        
            
    @staticmethod
    def get_by_id(id):
        try:
            observation = Observation.query.get(id)
            if observation:
                # Informações do grupo - usando a estrutura que já estava funcionando
                group_info = None
                if observation.group:
                    group_info = {
                        'id': observation.group.id,
                        'description': observation.group.description,
                        # Nota: Se Group não tiver relação direta com Grouptype,
                        # usamos o grouptypeId da Observation
                        'grouptypeId': observation.grouptypeId,
                        'grouptypeDescription': observation.grouptype.description if observation.grouptype else None,
                        'createAt': observation.group.createAt.isoformat() if observation.group.createAt else None,
                        'updateAt': observation.group.updateAt.isoformat() if observation.group.updateAt else None
                    }
                
                return jsonify({
                    'id': observation.id,
                    'nid': observation.nid,
                    'fullname': observation.fullname,
                    'gender': observation.gender,
                    'age': observation.age,
                    'contact': observation.contact,
                    'occupation': observation.occupation,
                    'datainiciotarv': observation.datainiciotarv.isoformat() if observation.datainiciotarv else None,
                    'datalevantamento': observation.datalevantamento.isoformat() if observation.datalevantamento else None,
                    'dataproximolevantamento': observation.dataproximolevantamento.isoformat() if observation.dataproximolevantamento else None,
                    'dataconsulta': observation.dataconsulta.isoformat() if observation.dataconsulta else None,
                    'dataproximaconsulta': observation.dataproximaconsulta.isoformat() if observation.dataproximaconsulta else None,
                    'dataalocacao': observation.dataalocacao.isoformat() if observation.dataalocacao else None,
                    'dataenvio': observation.dataenvio.isoformat() if observation.dataenvio else None,
                    'smssendernumber': observation.smssendernumber,
                    'smssuporternumber': observation.smssuporternumber,
                    'dataprimeiracv': observation.dataprimeiracv.isoformat() if observation.dataprimeiracv else None,
                    'valorprimeiracv': observation.valorprimeiracv,
                    'dataultimacv': observation.dataultimacv.isoformat() if observation.dataultimacv else None,
                    'valorultimacv': observation.valorultimacv,
                    'linhaterapeutica': observation.linhaterapeutica,
                    'regime': observation.regime,
                    'status': observation.status,
                    'smsStatus': observation.smsStatus,
                    'stateId': observation.stateId,
                    'textmessageId': observation.textmessageId,
                    'grouptypeId': observation.grouptypeId,
                    'groupId': observation.groupId,
                    'locationId': observation.locationId,
                    'userId': observation.userId,
                    'createAt': observation.createAt.isoformat() if observation.createAt else None,
                    'updateAt': observation.updateAt.isoformat() if observation.updateAt else None,
                    
                    # 🔥 Informações relacionadas
                    'state': {'id': observation.state.id, 'description': observation.state.description} if observation.state else None,
                    'textmessage': {'id': observation.textmessage.id, 'messagetext': observation.textmessage.messagetext} if observation.textmessage else None,
                    'grouptype': {'id': observation.grouptype.id, 'description': observation.grouptype.description} if observation.grouptype else None,
                    'group': group_info,  # Usando as informações detalhadas do grupo
                    'location': {'id': observation.location.id, 'name': observation.location.name} if observation.location else None,
                    'user': {'id': observation.user.id, 'fullname': observation.user.fullname} if observation.user else None
                }), 200
            return jsonify({'message': 'Observation not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()
            
            # Validação dos campos obrigatórios
            required_fields = ['nid', 'fullname', 'gender', 'age', 'contact', 'occupation',
                             'datainiciotarv', 'datalevantamento', 'dataproximolevantamento',
                             'dataconsulta', 'dataproximaconsulta', 'dataalocacao', 'dataenvio',
                             'smssendernumber', 'smssuporternumber', 'dataprimeiracv', 'valorprimeiracv',
                             'dataultimacv', 'valorultimacv', 'linhaterapeutica', 'regime','status','smsStatus'
                             'stateId', 'textmessageId', 'grouptypeId', 'groupId', 'locationId', 'userId']
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

            # Verifica se as FKs existem
            related_models = {
                'stateId': State,
                'textmessageId': Textmessage,
                'grouptypeId': Grouptype,
                'groupId': Group,
                'locationId': Location,
                'userId': User
            }

            for field, model in related_models.items():
                if not model.query.get(data[field]):
                    return jsonify({'message': f'{model.__name__} with id {data[field]} not found'}), 404

            # Cria nova observação
            new_observation = Observation(
                nid=data['nid'],
                fullname=data['fullname'],
                gender=data['gender'],
                age=data['age'],
                contact=data['contact'],
                occupation=data['occupation'],
                datainiciotarv=datetime.fromisoformat(data['datainiciotarv']),
                datalevantamento=datetime.fromisoformat(data['datalevantamento']),
                dataproximolevantamento=datetime.fromisoformat(data['dataproximolevantamento']),
                dataconsulta=datetime.fromisoformat(data['dataconsulta']),
                dataproximaconsulta=datetime.fromisoformat(data['dataproximaconsulta']),
                dataalocacao=datetime.fromisoformat(data['dataalocacao']),
                dataenvio=datetime.fromisoformat(data['dataenvio']),
                smssendernumber=data['smssendernumber'],
                smssuporternumber=data['smssuporternumber'],
                dataprimeiracv=datetime.fromisoformat(data['dataprimeiracv']),
                valorprimeiracv=data['valorprimeiracv'],
                dataultimacv=datetime.fromisoformat(data['dataultimacv']),
                valorultimacv=data['valorultimacv'],
                linhaterapeutica=data['linhaterapeutica'],
                regime=data['regime'],
                status=data['status'],
                smsStatus=data['smsStatus'],
                stateId=data['stateId'],
                textmessageId=data['textmessageId'],
                grouptypeId=data['grouptypeId'],
                groupId=data['groupId'],
                locationId=data['locationId'],
                userId=data['userId']
            )

            db.session.add(new_observation)
            db.session.commit()

            return jsonify({
                'id': new_observation.id,
                'message': 'Observation created successfully'
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(id):
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400

            # 1) Campos simples
            simple_fields = [
                'fullname', 'gender', 'age', 'contact', 'occupation',
                'smssendernumber', 'smssuporternumber', 'linhaterapeutica', 'regime',
                'smsStatus'
            ]
            for field in simple_fields:
                if field in data:
                    setattr(observation, field, data[field])

            # 2) Campos de data
            date_fields = [
                'datainiciotarv', 'datalevantamento', 'dataproximolevantamento',
                'dataconsulta', 'dataproximaconsulta', 'dataalocacao', 'dataenvio',
                'dataprimeiracv', 'dataultimacv'
            ]
            for field in date_fields:
                if field in data and data[field]:
                    setattr(observation, field, datetime.fromisoformat(data[field]))

            # 3) Campos numéricos
            if 'valorprimeiracv' in data:
                observation.valorprimeiracv = data['valorprimeiracv']
            if 'valorultimacv' in data:
                observation.valorultimacv = data['valorultimacv']

            # 4) Relacionamentos (FKs)
            fk_fields = {
                'stateId': 'state_id',
                'textmessageId': 'textmessage_id',
                'grouptypeId': 'grouptype_id',
                'groupId': 'group_id',
                'locationId': 'location_id',
                'userId': 'user_id'
            }

            for field, column_name in fk_fields.items():
                if field in data:
                    setattr(observation, column_name, data[field])

            # Atualiza timestamp
            observation.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'message': 'Observation updated successfully',
                'id': observation.id
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def confirm_action(id):
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400

            if 'stateId' not in data or 'textmessageId' not in data:
                return jsonify({'message': 'stateId and textmessageId are required'}), 400

            # Atualiza os campos principais
            observation.stateId = int(data['stateId'])
            observation.textmessageId = int(data['textmessageId'])
            observation.updateAt = datetime.utcnow()

            # Atualiza o campo status com o valor do State
            from models import State  # ou ajuste conforme o caminho do seu modelo
            state = State.query.get(int(data['stateId']))
            if state:
                observation.status = state.description  # ou o campo que representa o nome do estado

            db.session.commit()

            return jsonify({'message': 'Action confirmed successfully'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update_message_status(id):
        """Endpoint específico para atualizar o status da mensagem"""
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400

            # Campos obrigatórios para atualização de status
            required_fields = ['stateId', 'textmessageId']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

            # Atualiza os campos de status
            observation.stateId = int(data['stateId'])
            observation.textmessageId = int(data['textmessageId'])
            observation.updateAt = datetime.utcnow()

            # Atualiza o campo status com a descrição do State
            state = State.query.get(int(data['stateId']))
            if state:
                observation.status = state.description

            # Se houver data de envio no request, atualiza também
            if 'dataenvio' in data and data['dataenvio']:
                observation.dataenvio = datetime.fromisoformat(data['dataenvio'])

            # Se houver flag de sucesso/falha
            if 'message_sent' in data:
                # Aqui você pode adicionar lógica adicional baseada no sucesso/falha do envio
                pass

            db.session.commit()

            return jsonify({
                'message': 'Message status updated successfully',
                'id': observation.id,
                'status': observation.status,
                'stateId': observation.stateId,
                'textmessageId': observation.textmessageId
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update_message_status_simplified(id):
        """Endpoint específico para atualizar apenas status e smsStatus"""
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400

            # Campos que podem ser atualizados
            updatable_fields = ['status', 'smsStatus']
            
            # Verifica se pelo menos um dos campos está presente
            if not any(field in data for field in updatable_fields):
                return jsonify({
                    'message': f'No updatable fields provided. Available fields: {", ".join(updatable_fields)}'
                }), 400

            # Atualiza apenas os campos fornecidos
            if 'status' in data:
                observation.status = data['status']
            
            if 'smsStatus' in data:
                observation.smsStatus = data['smsStatus']

            # Atualiza a data de modificação
            observation.updateAt = datetime.utcnow()

            db.session.commit()

            return jsonify({
                'message': 'Message status updated successfully',
                'id': observation.id,
                'updated_fields': {
                    'status': observation.status if 'status' in data else 'unchanged',
                    'smsStatus': observation.smsStatus if 'smsStatus' in data else 'unchanged'
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def update_group(id):
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            data = request.get_json()
            if not data:
                return jsonify({'message': 'No data provided'}), 400

            # Campos obrigatórios
            if 'groupId' not in data or 'textmessageId' not in data:
                return jsonify({'message': 'groupId and textmessageId are required'}), 400

            # Atualizar campos obrigatórios
            observation.groupId = int(data['groupId'])
            observation.textmessageId = int(data['textmessageId'])
            
            # Atualizar status se fornecido
            if 'stateId' in data and data['stateId']:
                observation.stateId = int(data['stateId'])
                
            # Atualizar outros campos opcionais
            if 'grouptypeId' in data and data['grouptypeId']:
                observation.grouptypeId = int(data['grouptypeId'])
                
            if 'userobservacao' in data and data['userobservacao']:
                observation.userobservacao = data['userobservacao']
                
            if 'observation' in data and data['observation']:
                observation.observation = data['observation']
            
            # Atualizar timestamp
            observation.updateAt = datetime.utcnow()

            db.session.commit()
            
            # Retornar dados atualizados
            return jsonify({
                'message': 'Observation updated successfully',
                'data': {
                    'id': observation.id,
                    'groupId': observation.groupId,
                    'stateId': observation.stateId,
                    'textmessageId': observation.textmessageId,
                    'grouptypeId': observation.grouptypeId,
                    'updateAt': observation.updateAt.isoformat()
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def delete(id):
        try:
            observation = Observation.query.get(id)
            if not observation:
                return jsonify({'message': 'Observation not found'}), 404

            db.session.delete(observation)
            db.session.commit()

            return jsonify({'message': 'Observation deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500