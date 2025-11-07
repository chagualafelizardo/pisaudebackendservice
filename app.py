import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_babelex import Babel, gettext as _
from config import Config
from models import db, Observation, User
from models import User, UserComponente
from werkzeug.security import check_password_hash
import os

# -------------------------------
# Configuração de Logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s'
)

logger = logging.getLogger(__name__)

# -------------------------------
# Inicialização da App Flask
# -------------------------------
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'sua_chave_secreta'

# Inicialização do SQLAlchemy
db.init_app(app)

# Inicialização do Babel (idiomas)
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en']
babel = Babel(app)

# -------------------------------
# Importação de Blueprints
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
from routes.EspecialidadeSaudeRoutes import especialidade_saude_bp
from routes.CandidatoRoutes import candidato_bp
from routes.TipoLicencaRoutes import tipo_licenca_bp
from routes.PaisRoutes import pais_bp
from routes.FormacaoRoutes import formacao_bp
from routes.LicencaRoutes import licenca_bp
from routes.DespachoRoutes import despacho_bp
from routes.ProvinciaRoutes import provincia_bp
from routes.ArmazemRoutes import armazem_bp
from routes.ItemRoutes import item_bp
from routes.ComponenteRoutes import componente_bp
from routes.UserComponenteRoute import usercomponente_bp
from routes.PortoRoutes import porto_bp
from routes.ItemLocationNecessidadeRoutes import necessidade_bp
from routes.ItemHistoricoController import historico_bp
from routes.DistribuicaoRoutes import distribuicao_bp
from routes.TipoItemRoutes import tipo_item_bp
from routes.NotaEnvioRoutes import nota_envio_bp
from routes.NotaEnvioItemRoutes import nota_envio_item_bp
from routes.NotaEnvioDocumentRoutes import nota_envio_document_bp

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
    transferencia_bp, especialidade_saude_bp, candidato_bp, tipo_licenca_bp,
    pais_bp, formacao_bp, despacho_bp, licenca_bp, provincia_bp, armazem_bp,
    item_bp, componente_bp, usercomponente_bp, porto_bp, necessidade_bp,
    historico_bp, distribuicao_bp, tipo_item_bp, nota_envio_bp,
    nota_envio_item_bp, nota_envio_document_bp
]

for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

# -------------------------------
# Idioma (Babel)
# -------------------------------
@babel.localeselector
def get_locale():
    return session.get('lang') or request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('dashboard'))

# -------------------------------
# Context Processor — info do usuário
# -------------------------------
@app.context_processor
def inject_user_components():
    user_id = session.get('user_id')
    user_components = []
    username = ''
    location_name = ''

    if user_id:
        user = User.query.get(user_id)
        if user:
            username = getattr(user, 'fullname', user.username)
            location_name = getattr(user.location, 'name', '') if getattr(user, 'location', None) else ''

            componentes = UserComponente.query.filter_by(user_id=user_id).all()
            user_components = [uc.componente.descricao for uc in componentes if uc.componente]

    return dict(
        username=username,
        location_name=location_name,
        user_components=user_components,
        current_year=datetime.now().year
    )

# -------------------------------
# Rotas Frontend (HTML)
# -------------------------------
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/dashboarddistribuicao')
def dashboard_distribuicao():
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboarddistribuicao.html')

@app.route('/content/<page>')
def content(page):
    # Converter para minúsculas para evitar problemas de case sensitivity
    page = page.lower()
    
    # Verificar autenticação
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    # Lista de páginas permitidas
    allowed_pages = [
        # Dashboard
        'dashboard', 'dashboarddistribuicao',
        
        # Menu Registo
        'provincia', 'location', 'subunidade', 'portatestagem', 'keypopulation',
        'grouptypes', 'group', 'states', 'textmessage', 'ramo', 'funcao',
        'especialidade', 'subespecialidade', 'pais',
        
        # Recursos Humanos
        'patent', 'person', 'formaprestacaoservico', 'situacaogeral', 
        'situacaoprestacaoservico', 'tipolicenca', 'licenca', 'despacho',
        
        # Gestão de Alocação
        'afetacao', 'transferencia',
        
        # Gestão de Formações
        'especialidadesaude', 'formacao', 'candidato',
        
        # Items Tracking
        'porto', 'tipoitem', 'notaenvio', 'armazem', 'item', 'distribuicao',
        
        # Alo-Saúde
        'alosaude',
        
        # Resources Mapping
        'resource', 'resourcetype', 'mapping',
        
        # Grupos Alo-Saúde
        'iniciotarv', 'adesaotarv', 'cargaviral', 'faltosos', 'abandonos', 'observations',
        
        # User Management
        'user', 'roles', 'componente',
        
        # Configurações
        'register', 'settings'
    ]
    
    if page not in allowed_pages:
        flash(f'A página "{page}" não existe ou não está disponível.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        return render_template(f'{page}.html')
    except Exception as e:
        logger.error(f"Erro ao carregar template '{page}.html': {str(e)}")
        flash(f'Erro ao carregar a página {page}.', 'danger')
        return redirect(url_for('dashboard'))

# -------------------------------
# Login / Logout
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
            session['location_name'] = user.location.name if user.location else ''
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sessão terminada com sucesso.', 'info')
    return redirect(url_for('login'))

# -------------------------------
# Rota de importação de Observações (API)
# -------------------------------
@app.route('/api/observations/import', methods=['POST'])
def import_observations():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
        
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON or empty payload'}), 400

    stateId = data.get("stateID")
    grouptypeId = data.get("groupTypeID")
    observations = data.get("observations", [])

    batch, imported_count, errors = [], 0, []
    BATCH_SIZE = 50

    for idx, row in enumerate(observations):
        try:
            obs = Observation(
                nid=row.get('nid', ''),
                fullname=row.get('fullname', ''),
                gender=row.get('gender', ''),
                age=row.get('age', 0),
                contact=row.get('contact', ''),
                occupation=row.get('occupation', ''),
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
            batch.append(obs)
            imported_count += 1
            if len(batch) >= BATCH_SIZE:
                db.session.add_all(batch)
                db.session.flush()
                batch = []
        except Exception as e:
            errors.append({'row': idx, 'error': str(e)})

    if batch:
        db.session.add_all(batch)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database commit failed', 'details': str(e)}), 500

    return jsonify({'message': 'Import completed', 'imported_count': imported_count, 'errors': errors}), 200

# -------------------------------
# Error Handlers
# -------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Página Não Encontrada</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="alert alert-warning text-center">
                <h1>🔍 404 - Página Não Encontrada</h1>
                <p>A página solicitada não existe.</p>
                <a href="/dashboard" class="btn btn-primary">Voltar ao Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Erro Interno</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="alert alert-danger text-center">
                <h1>🚨 500 - Erro Interno do Servidor</h1>
                <p>Ocorreu um erro interno. Tente novamente mais tarde.</p>
                <a href="/dashboard" class="btn btn-primary">Voltar ao Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """, 500

# Rota para favicon
@app.route('/favicon.ico')
def favicon():
    return '', 204

# -------------------------------
# Inicialização da App
# -------------------------------
if __name__ == '__main__':
    logger.info("🚀 Iniciando aplicação PI-SAÚDE...")
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host="0.0.0.0", port=5000)