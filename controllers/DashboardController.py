from flask import jsonify, request
from datetime import datetime, timedelta
from models import db, Observation, State, Textmessage, Location
from sqlalchemy import and_, or_

class DashboardController:
    @staticmethod
    def get_dashboard_data():
        try:
            # Parâmetros de filtro
            start_date = request.args.get('startDate')
            end_date = request.args.get('endDate')
            location_id = request.args.get('locationId')
            
            # Query base
            query = Observation.query
            
            # Aplicar filtros
            if start_date:
                start_date = datetime.fromisoformat(start_date)
                query = query.filter(Observation.createAt >= start_date)
            
            if end_date:
                end_date = datetime.fromisoformat(end_date)
                query = query.filter(Observation.createAt <= end_date)
            
            if location_id:
                query = query.filter(Observation.locationId == int(location_id))
            
            all_observations = query.all()
            
            # Estatísticas gerais
            stats = {
                'totalPatients': len(all_observations),
                'levantamentosCount': 0,
                'faltososCount': 0,
                'chamadasCount': 0,
                'visitasCount': 0
            }
            
            # Classificar pacientes
            levantamentos = []
            faltosos = []
            chamadas = []
            visitas = []
            
            for obs in all_observations:
                # 1. Pacientes para Levantamento (próxima semana)
                if obs.dataproximolevantamento:
                    next_week = datetime.now() + timedelta(days=7)
                    if obs.dataproximolevantamento <= next_week:
                        levantamentos.append(obs)
                        stats['levantamentosCount'] += 1
                
                # 2. Pacientes Faltosos (última CV há mais de 30 dias)
                if obs.dataultimacv:
                    thirty_days_ago = datetime.now() - timedelta(days=30)
                    if obs.dataultimacv <= thirty_days_ago:
                        faltosos.append(obs)
                        stats['faltososCount'] += 1
                
                # 3. Pacientes para Chamadas (próxima consulta próxima)
                if obs.dataproximaconsulta:
                    next_week = datetime.now() + timedelta(days=7)
                    if obs.dataproximaconsulta <= next_week:
                        chamadas.append(obs)
                        stats['chamadasCount'] += 1
                
                # 4. Pacientes para Visitas (observações específicas)
                if obs.observation and any(keyword in obs.observation.lower() for keyword in ['visita', 'domiciliar', 'casa', 'domicilio']):
                    visitas.append(obs)
                    stats['visitasCount'] += 1
            
            # Dados semanais (últimas 4 semanas)
            weekly_stats = DashboardController.get_weekly_stats(all_observations)
            weekly_trend = DashboardController.get_weekly_trend(all_observations)
            
            return jsonify({
                'stats': stats,
                'weeklyStats': weekly_stats,
                'weeklyTrend': weekly_trend,
                'levantamentos': [DashboardController.obs_to_dict(obs) for obs in levantamentos[:10]],  # Top 10
                'faltosos': [DashboardController.obs_to_dict(obs) for obs in faltosos[:10]],
                'chamadas': [DashboardController.obs_to_dict(obs) for obs in chamadas[:10]],
                'visitas': [DashboardController.obs_to_dict(obs) for obs in visitas[:10]]
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def get_weekly_stats(observations):
        """Estatísticas da semana atual"""
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        week_end = week_start + timedelta(days=6)
        
        week_observations = [obs for obs in observations 
                           if week_start <= obs.createAt <= week_end]
        
        return {
            'levantamentos': len([obs for obs in week_observations 
                                if obs.dataproximolevantamento and 
                                obs.dataproximolevantamento <= week_end]),
            'faltosos': len([obs for obs in week_observations 
                           if obs.dataultimacv and 
                           (datetime.now() - obs.dataultimacv).days > 30]),
            'chamadas': len([obs for obs in week_observations 
                           if obs.dataproximaconsulta and 
                           obs.dataproximaconsulta <= week_end]),
            'visitas': len([obs for obs in week_observations 
                          if obs.observation and 
                          any(keyword in obs.observation.lower() 
                              for keyword in ['visita', 'domiciliar'])])
        }
    
    @staticmethod
    def get_weekly_trend(observations):
        """Tendência das últimas 4 semanas"""
        trends = {
            'weeks': [],
            'levantamentos': [],
            'faltosos': [],
            'chamadas': []
        }
        
        for i in range(4):
            week_num = 4 - i
            week_start = datetime.now() - timedelta(weeks=week_num)
            week_end = week_start + timedelta(days=6)
            
            week_obs = [obs for obs in observations 
                       if week_start <= obs.createAt <= week_end]
            
            trends['weeks'].append(f"Sem {week_num}")
            trends['levantamentos'].append(len([obs for obs in week_obs 
                                              if obs.dataproximolevantamento]))
            trends['faltosos'].append(len([obs for obs in week_obs 
                                         if obs.dataultimacv and 
                                         (week_end - obs.dataultimacv).days > 30]))
            trends['chamadas'].append(len([obs for obs in week_obs 
                                         if obs.dataproximaconsulta]))
        
        return trends
    
    @staticmethod
    def obs_to_dict(observation):
        """Converte Observation para dict"""
        return {
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
            'dataultimacv': observation.dataultimacv.isoformat() if observation.dataultimacv else None,
            'valorultimacv': observation.valorultimacv,
            'observation': observation.observation,
            'location': {
                'id': observation.location.id,
                'name': observation.location.name
            } if observation.location else None,
            'state': {
                'id': observation.state.id,
                'description': observation.state.description
            } if observation.state else None
        }
