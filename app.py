from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User  # Certifique-se que User tem username e password
from config import Config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from models import Observation, State, Textmessage, Grouptype, Group, Location, User
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
    user_bp, keypopulation_bp, portatestagem_bp
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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        return render_template('dashboard.html', username=session['username'])
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500

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
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    try:
        return render_template('settings.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500
    
# Rotas para upload de Excel
@app.route('/iniciotarv')
def iniciotarv():
    try:
        return render_template('iniciotarv.html')
    except Exception as e:
        return f"Erro ao carregar dashboard: {str(e)}", 500
    

# ------- Seccao para importacao dos ficheiros excel -------------
# Codigo para importar dados vindo do excel ou csv
@app.route('/api/observations/import', methods=['POST'])
def import_observations():
    data = request.get_json()
    logging.info(f"Received data: {data[:3]}... total rows: {len(data)}")
    imported_count = 0
    errors = []
    BATCH_SIZE = 50
    batch = []


    for idx, row in enumerate(data):
        try:
            observation = Observation(
                nid=row.get('nid', ''),
                fullname=row.get('fullname', ''),
                gender=row.get('gender', ''),
                age=row.get('age', 0),
                contact=row.get('contact', '0'),
                occupation='',
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
                stateId=1,
                textmessageId=1,
                grouptypeId=1,
                groupId=1,
                locationId=1,
                userId=1
            )
            batch.append(observation)
            imported_count += 1

            if len(batch) >= BATCH_SIZE:
                db.session.add_all(batch)
                db.session.flush()  # não commita ainda
                batch = []

        except Exception as e:
            logging.error(f"Error in row {idx}: {str(e)}")
            errors.append({'row': idx, 'error': str(e)})

    # salvar qualquer sobra
    if batch:
        db.session.add_all(batch)

    # commit final
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database commit failed: {str(e)}")
        return jsonify({'error': 'Database commit failed', 'details': str(e)}), 500

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
    app.run(debug=True)
