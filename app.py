# app.py (REFATORADO)
import logging
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_babelex import Babel, gettext as _
from config import Config
from models import db, Observation, User, Location
from models import User, UserComponente
from werkzeug.security import check_password_hash
from flask_cors import CORS

# 🔥 IMPORTE O BOT
from bot.jhpiego_bot import JhpiegoBot
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

# 🔹 Configuração CORS
CORS(app)

# Inicialização do SQLAlchemy
db.init_app(app)

# Instância global do bot
jhpiego_bot = JhpiegoBot()

# Inicialização do Babel (idiomas)
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en']
babel = Babel(app)

# -------------------------------
# Importação de Blueprints (MANTIDO)
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
from routes.ItensPendentesRoutes import itens_pendentes_bp
from routes.ItensSolicitadosRoutes import items_solicitados_bp
from routes.AiRoutes import ai_bp

# -------------------------------
# Registro de Blueprints (MANTIDO)
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
    nota_envio_item_bp, nota_envio_document_bp, itens_pendentes_bp,
    items_solicitados_bp, ai_bp
]

for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

# -------------------------------
# 🔥 ENDPOINT SIMPLIFICADO DO BOT
# -------------------------------
@app.route('/api/ai-query', methods=['POST'])
def ai_query():
    """Endpoint para consultas do Jhpiego Bot"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"response": "Por favor, forneça uma mensagem."}), 400
        
        question = data['message'].strip()
        
        # 🔥 USAR O BOT PARA PROCESSAR
        result = jhpiego_bot.process_query(question)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro no endpoint AI: {e}")
        return jsonify({
            "response": "Ocorreu um erro ao processar sua pergunta. Tente novamente.",
            "topic": None,
            "source": None
        }), 500

# -------------------------------
# 🔥 NOVO ENDPOINT: Status do Bot
# -------------------------------
@app.route('/api/bot-status', methods=['GET'])
def bot_status():
    """Retorna status do bot e documentos carregados"""
    try:
        upload_dir = jhpiego_bot.UPLOAD_DIR
        documents = []
        
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                if filename.endswith(('.txt', '.pdf', '.docx', '.xlsx')):
                    documents.append({
                        'name': filename,
                        'size': os.path.getsize(os.path.join(upload_dir, filename))
                    })
        
        return jsonify({
            'status': 'active',
            'documents_loaded': len(documents),
            'documents': documents,
            'topics_supported': list(jhpiego_bot.TOPIC_KEYWORDS.keys())
        })
        
    except Exception as e:
        logger.error(f"❌ Erro no status do bot: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# -------------------------------
# 🔥 NOVO ENDPOINT: Upload de Documentos
# -------------------------------
@app.route('/api/upload-document', methods=['POST'])
def upload_document():
    """Endpoint para upload de documentos para o bot"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nome de arquivo vazio'}), 400
        
        if file and file.filename.endswith(('.txt', '.pdf', '.docx', '.xlsx')):
            filename = file.filename
            filepath = os.path.join(jhpiego_bot.UPLOAD_DIR, filename)
            file.save(filepath)
            
            logger.info(f"✅ Documento salvo: {filename}")
            return jsonify({'message': f'Documento {filename} carregado com sucesso'})
        else:
            return jsonify({'error': 'Tipo de arquivo não suportado'}), 400
            
    except Exception as e:
        logger.error(f"❌ Erro no upload: {e}")
        return jsonify({'error': str(e)}), 500

# -------------------------------
# Resto do código (MANTIDO - idioma, context processor, rotas frontend, etc.)
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

# Context Processor — info do usuário (MANTIDO)
@app.context_processor
def inject_user_components():
    user_id = session.get('user_id')
    username = ''
    location_name = ''
    user_menus = []
    user_component_names = []

    if user_id:
        user = User.query.get(user_id)
        if user:
            username = getattr(user, 'fullname', user.username)
            location_name = getattr(user.location, 'name', '') if getattr(user, 'location', None) else ''
            componentes = UserComponente.query.filter_by(user_id=user_id).all()
            user_component_names = [uc.componente.descricao for uc in componentes if uc.componente]
            user_menus = get_user_menus(user_id)

    return dict(
        username=username,
        location_name=location_name,
        user_components=user_component_names,
        user_menus=user_menus,
        current_year=datetime.now().year
    )

# Rotas Frontend (MANTIDO)
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    total_users = User.query.count()
    total_locations = Location.query.count()
    return render_template('dashboard.html', 
                         total_users=total_users,
                         total_locations=total_locations,
                         total_records=0,
                         system_activity='Online')

@app.route('/content/<page>')
def content(page):
    # Converter para minúsculas
    page = page.lower()
    
    # Verificar autenticação
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    # Páginas básicas sempre permitidas
    if page in ['dashboard', 'dashboarddistribuicao','dashboarddoddistribuicao','pisaudedashboard']:
        try:
            return render_template(f'{page}.html')
        except Exception as e:
            logger.error(f"Erro ao carregar template '{page}.html': {str(e)}")
            flash(f'Erro ao carregar a página {page}.', 'danger')
            return redirect(url_for('dashboard'))
    
    # Verificar se a página é permitida para o usuário
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if user:
        # Buscar menus permitidos para o usuário
        user_menus = get_user_menus(user_id)
        
        # Mapeamento de páginas para menus principais
        page_to_menu = {
            # Gestão de Formações
            # 'especialidadesaude': 'gestaoFormacaoMenu',
            # 'formacao': 'gestaoFormacaoMenu', 
            # 'candidato': 'gestaoFormacaoMenu',
            
            # Resources Mapping
            # 'resource': 'mappingMenu',
            # 'resourcetype': 'mappingMenu',
            # 'mapping': 'mappingMenu',
            
            # Gestão de Alocação
            # 'afetacao': 'gestaoAlocacaoMenu',
            # 'transferencia': 'gestaoAlocacaoMenu',
            
            # Items Tracking
            # 'porto': 'trackingMenu',
            # 'tipoitem': 'trackingMenu',
            # 'notaenvio': 'trackingMenu',
            # 'armazem': 'trackingMenu',
            # 'item': 'trackingMenu',
            # 'distribuicao': 'trackingMenu',
            
            # Alo-Saúde
            # 'alosaude': 'alosaudeMenu',
            
            # Menu Registo
            # 'provincia': 'registoMenu',
            # 'location': 'registoMenu',
            # 'subunidade': 'registoMenu',
            # 'portatestagem': 'registoMenu',
            # 'keypopulation': 'registoMenu',
            # 'grouptypes': 'registoMenu',
            # 'group': 'registoMenu',
            # 'states': 'registoMenu',
            # 'textmessage': 'registoMenu',
            # 'ramo': 'registoMenu',
            # 'funcao': 'registoMenu',
            # 'especialidade': 'registoMenu',
            # 'subespecialidade': 'registoMenu',
            # 'pais': 'registoMenu',
            
            # Recursos Humanos
            # 'patent': 'rhMenu',
            # 'person': 'rhMenu',
            # 'formaprestacaoservico': 'rhMenu',
            # 'situacaogeral': 'rhMenu',
            # 'situacaoprestacaoservico': 'rhMenu',
            # 'tipolicenca': 'rhMenu',
            # 'licenca': 'rhMenu',
            # 'despacho': 'rhMenu',
            
            # Grupos Alo-Saúde
            # 'iniciotarv': 'gruposAlosaudeMenus',
            # 'adesaotarv': 'gruposAlosaudeMenus',
            # 'cargaviral': 'gruposAlosaudeMenus',
            # 'faltosos': 'gruposAlosaudeMenus',
            # 'abandonos': 'gruposAlosaudeMenus',
            # 'observations': 'gruposAlosaudeMenus',
            # 'Modulo Alo-Saúde':'moduloAloSaude',
            
            # User Management
            # 'location':'locationMenu',
            # 'user': 'userMenu',
            # 'roles': 'userMenu',
            # 'componente': 'userMenu',
            # 'register': 'userMenu',
            # 'settings': 'userMenu'
        }
        
        # Verificar se a página é permitida
        if page in page_to_menu:
            required_menu = page_to_menu[page]
            
            # Verificar se o usuário tem o menu necessário
            if required_menu not in user_menus:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('dashboard'))
    
    try:
        return render_template(f'{page}.html')
    except Exception as e:
        logger.error(f"Erro ao carregar template '{page}.html': {str(e)}")
        flash(f'Erro ao carregar a página {page}.', 'danger')
        return redirect(url_for('dashboard'))

# Login / Logout (MANTIDO)
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

@app.route('/about')
def about():
    return render_template('about.html')

def get_user_menus(user_id):
    """Retorna lista de IDs de menus permitidos para o usuário (MANTIDO)"""
    user_menus = []
    componentes = UserComponente.query.filter_by(user_id=user_id).all()
    user_component_names = [uc.componente.descricao for uc in componentes if uc.componente]
    
    componente_to_menu = {
        'Formação': 'gestaoFormacaoMenu',
        'Mapeamento de recursos': 'mappingMenu', 
        'Afetação / Alocação': 'gestaoAlocacaoMenu',
        'Itens Traking': 'trackingMenu',
        'Alo-Saúde': 'alosaudeMenu',
        'Menu de registos': 'registoMenu',
        'Menu de Recursos Humanos': 'rhMenu',
        'Menus do usuário': 'userMenu',
        'Menus de localização': 'locationMenu',
        'Menus de grupos de alo saúde': 'gruposAlosaudeMenus',
        'Módulo Alo-Saúde': 'moduloAloSaude'
    }
    
    for component_name in user_component_names:
        if component_name in componente_to_menu:
            user_menus.append(componente_to_menu[component_name])
    
    return user_menus

# Rota de importação de Observações (MANTIDO)
@app.route('/api/observations/import', methods=['POST'])
def import_observations():
    # ... (código mantido igual)
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
                status='',
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

# Error Handlers (MANTIDO)
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

@app.route('/favicon.ico')
def favicon():
    return '', 204

# -------------------------------
# Inicialização da App
# -------------------------------
if __name__ == '__main__':
    logger.info("🚀 Iniciando aplicação PI-SAÚDE com Jhpiego Bot...")
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host="0.0.0.0", port=5000)