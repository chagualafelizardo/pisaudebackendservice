from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User
from config import Config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from models import Observation, State, Textmessage, Grouptype, Group, Location, User, Resource, ResourceType
import logging

# -------------------------------
# Importações dos Blueprints
# -------------------------------
from routes.ContactLinkRoutes import contactlink_bp
from routes.DailyRecordRoutes import dailyrecord_bp
from routes.ObservationRoutes import observation_bp
from routes.LocationRoutes import location_bp
from routes.RoleRoutes import role_bp
from routes.GroupRoutes import group_bp
from routes.GrouptyeRoutes import grouptype_bp
from routes.StateRoutes import state_bp
from routes.TextmessageRoute import textmessage_bp
from routes.UserRoleRoutes import userrole_bp
from routes.UserRoutes import user_bp
from routes.KeyPopulationRoutes import keypopulation_bp
from routes.PortaTestagemRoutes import portatestagem_bp
from routes.ResourceTypeRoutes import resourcetype_bp
from routes.ResourceRoutes import resource_bp
from routes.FormaPrestacaoServicoRoutes import forma_prestacao_servico_bp
from routes.PersonRoutes import person_bp
from routes.PatentRoutes import patent_bp
from routes.RamoRoutes import ramo_bp
from routes.SubunidadeRoutes import subunidade_bp
from routes.EspecialidadeRoutes import especialidade_bp
from routes.SubespecialidadeRoutes import subespecialidade_bp
from routes.SituacaoGeralRoutes import situacao_geral_bp
from routes.FuncaoRoutes import funcao_bp
from routes.SituacaoPrestacaoServicoRoutes import situacao_prestacao_servico_bp
from routes.AfetacaoRoutes import afetacao_bp
from routes.TransferenciaRoutes import transferencia_bp

# -------------------------------
# Inicialização da App Flask
# -------------------------------
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'sua_chave_secreta'  # Necessário para sessões

# Inicialização do SQLAlchemy
db.init_app(app)

# Definicao de constantes
state_default_id = 9  # ID default para State "inicial"

# -------------------------------
# Registro de Blueprints (API)
# -------------------------------
blueprints = [
    contactlink_bp, dailyrecord_bp, observation_bp, location_bp, role_bp,
    group_bp, grouptype_bp, state_bp, textmessage_bp, userrole_bp,
    user_bp, keypopulation_bp, portatestagem_bp, resource_bp,
    resourcetype_bp, forma_prestacao_servico_bp, person_bp, patent_bp,
    ramo_bp, subunidade_bp, especialidade_bp, subespecialidade_bp,
    situacao_geral_bp, funcao_bp, situacao_prestacao_servico_bp, afetacao_bp,
    transferencia_bp
]

for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

# -------------------------------
# Rotas do Frontend (Renderização)
# -------------------------------
@app.route('/')
@app.route('/api')
def api():
    try:
        return render_template('api.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500

@app.route('/dashboard')
def dashboard():
    if 'userId' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('login'))
    
    username = session.get('username')
    location_name = session.get('locationName')

    return render_template('dashboard.html', username=username, location_name=location_name)

@app.route('/content/<page>')
def content(page):
    try:
        return render_template(f'{page}.html')
    except Exception as e:
        return f"Erro ao carregar a página '{page}': {str(e)}", 404

# -------------------------------
# Rotas de Login/Logout
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Aqui você busca o usuário no banco
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Salva informações do usuário na sessão
            session['userId'] = user.id
            session['username'] = user.username
            session['locationId'] = user.locationId  # assumindo que User tem location_id
            session['locationName'] = user.location.name  # se quiser exibir nome da unidade

            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/settings')
def settings():
    try:
        return render_template('settings.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ------- Seccao para importacao dos ficheiros excel -------------
# Rotas para upload de Excel: Pacientes Inicio ao TARV
@app.route('/iniciotarv')
def iniciotarv():
    try:
        return render_template('iniciotarv.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500
    
# Rotas para upload de Excel: Pacientes Adesao ao TARV
@app.route('/adesaotarv')
def adesaotarv():
    try:
        return render_template('adesaotarv.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500

# Rotas para upload de Excel: Pacientes Como Carva Viral
@app.route('/cargaviral')
def cargaviral():
    try:
        return render_template('cargaviral.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500

# Rotas para upload de Excel: Pacientes faltosos
@app.route('/faltosos')
def faltosos():
    try:
        return render_template('faltosos.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500

# Rotas para upload de Excel: Pacientes abandonos
@app.route('/abandonos')
def abandonos():
    try:
        return render_template('abandonos.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500
        
# Rotas para upload de Excel: Pacientes Marcados para o Levantamento de ARVs
@app.route('/marcadoslevantamento')
def marcadoslevantamento():
    try:
        return render_template('marcadoslevantamento.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500

# Rotas para upload de Excel: Pacientes outros
@app.route('/outros')
def outros():
    try:
        return render_template('outros.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500
    
# Codigo para importar dados vindo do excel ou csv
@app.route('/api/observations/import', methods=['POST'])
def import_observations():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON or empty payload'}), 400

    stateId = data.get("stateID")
    grouptypeId = data.get("groupTypeID")
    observations = data.get("observations", [])

    logging.info(f"Received observations sample: {observations[:3]}... total rows: {len(observations)}")

    imported_count = 0
    errors = []
    BATCH_SIZE = 50
    batch = []

    for idx, row in enumerate(observations):
        try:
            observation = Observation(
                nid=row.get('nid', ''),
                fullname=row.get('fullname', ''),
                gender=row.get('gender', ''),
                age=row.get('age', 0),
                contact=row.get('contact', '0'),
                occupation=row.get('occupation', ''),  # se estiver vazio, ok
                datainiciotarv=datetime.now(),
                datalevantamento=datetime.now(),
                dataproximolevantamento=datetime.now(),
                dataconsulta=datetime.now(),
                dataproximaconsulta=datetime.now(),
                dataalocacao=datetime.now(),
                dataenvio=datetime.now(),
                smssendernumber='',
                smssuporternumber='',
                dataprimeiracv=datetime.now(),
                valorprimeiracv=0,
                dataultimacv=datetime.now(),
                valorultimacv=0,
                linhaterapeutica='',
                regime='',
                stateId=stateId,
                textmessageId=1,
                grouptypeId=grouptypeId,
                groupId=1,
                locationId=1,
                userId=1
            )
            batch.append(observation)
            imported_count += 1

            if len(batch) >= BATCH_SIZE:
                db.session.add_all(batch)
                db.session.flush()
                batch = []

        except Exception as e:
            logging.error(f"Error in row {idx}: {str(e)}")
            errors.append({'row': idx, 'error': str(e)})

    if batch:
        db.session.add_all(batch)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database commit failed: {str(e)}")
        return jsonify({'error': 'Database commit failed', 'details': str(e)}), 500

    return jsonify({
        'message': 'Import completed successfully',
        'imported_count': imported_count,
        'errors': errors
    }), 200


# -------------------------------
# Context Processor
# -------------------------------
@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

# -------------------------------
# Inicialização da App
# -------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria tabelas
    app.run(debug=True, host="0.0.0.0", port=5000)
