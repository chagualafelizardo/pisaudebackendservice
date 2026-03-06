# app.py (CORRIGIDO)
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
from flask_login import LoginManager, login_required, current_user
from datetime import datetime, timedelta
import re

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

# --- Flask-Login configuration ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 🔹 Configuração CORS
# CORS(app)
CORS(app, supports_credentials=True, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

# Inicialização do SQLAlchemy
db.init_app(app)

# Instância global do bot
jhpiego_bot = JhpiegoBot()

# -------------------------------
# CONFIGURAÇÃO DO BABEL (IDIOMAS)
# -------------------------------
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en', 'es', 'fr']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

# Define o user_loader para carregar o usuário da sessão
@login_manager.user_loader
def load_user(user_id):
    print(f"🔍 load_user chamado com user_id={user_id}")
    from models import User
    return User.query.get(int(user_id))

# -------------------------------
# SELEÇÃO DE IDIOMA
# -------------------------------
@babel.localeselector
def get_locale():
    """Determina o idioma a ser usado para a requisição atual"""
    # 1. Verifica idioma definido na sessão
    if 'lang' in session:
        return session['lang']
    
    # 2. Verifica preferência do usuário logado
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and hasattr(user, 'language') and user.language:
            return user.language
    
    # 3. Usa idioma do navegador
    browser_lang = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
    return browser_lang or app.config['BABEL_DEFAULT_LOCALE']

# -------------------------------
# CONTEXT PROCESSOR PARA TEMPLATES (CORRIGIDO)
# -------------------------------
@app.context_processor
def inject_i18n():
    """Injeta variáveis de internacionalização nos templates"""
    return dict(
        _=_,  # Função gettext para traduções
        get_locale=get_locale,  # <-- ADICIONE ESTA LINHA
        current_locale=get_locale(),
        supported_locales=app.config['BABEL_SUPPORTED_LOCALES']
    )

# -------------------------------
# ROTA PARA ALTERAR IDIOMA
# -------------------------------
@app.route('/set_language/<lang>')
def set_language(lang):
    """Altera o idioma da aplicação"""
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
        
        # Atualiza preferência no banco se usuário estiver logado
        if 'user_id' in session:
            try:
                user = User.query.get(session['user_id'])
                if user and hasattr(user, 'language'):
                    user.language = lang
                    db.session.commit()
                    logger.info(f"Idioma atualizado para {lang} para usuário {user.username}")
            except Exception as e:
                logger.error(f"Erro ao atualizar idioma do usuário: {e}")
        
        flash(_('Idioma alterado para %(lang)s', lang=lang), 'success')
    
    # Redireciona para página anterior ou dashboard
    referrer = request.referrer
    if not referrer or referrer.endswith('/set_language/' + lang):
        referrer = url_for('dashboard')
    
    return redirect(referrer)

# -------------------------------
# API PARA OBTER IDIOMA ATUAL
# -------------------------------
@app.route('/api/current-language', methods=['GET'])
def get_current_language():
    """Retorna o idioma atual configurado"""
    return jsonify({
        'locale': get_locale(),
        'supported_locales': app.config['BABEL_SUPPORTED_LOCALES']
    })

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
from routes.AgendamentoRoutes import agendamento_bp
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
    items_solicitados_bp, agendamento_bp
]

for bp in blueprints:
    app.register_blueprint(bp, url_prefix='/api')

# -------------------------------
# 🔥 ENDPOINT DO BOT COM SUPORTE A IDIOMAS
# -------------------------------
@app.route('/api/ai-query', methods=['POST'])
def ai_query():
    """Endpoint para consultas do Jhpiego Bot com suporte a idiomas"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"response": _("Por favor, forneça uma mensagem.")}), 400
        
        question = data['message'].strip()
        user_lang = get_locale()  # Obtém idioma do usuário
        
        # 🔥 USAR O BOT PARA PROCESSAR
        result = jhpiego_bot.process_query(question)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro no endpoint AI: {e}")
        return jsonify({
            "response": _("Ocorreu um erro ao processar sua pergunta. Tente novamente."),
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
            return jsonify({'error': _('Nenhum arquivo enviado')}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': _('Nome de arquivo vazio')}), 400
        
        if file and file.filename.endswith(('.txt', '.pdf', '.docx', '.xlsx')):
            filename = file.filename
            filepath = os.path.join(jhpiego_bot.UPLOAD_DIR, filename)
            file.save(filepath)
            
            logger.info(f"✅ Documento salvo: {filename}")
            return jsonify({'message': _('Documento %(filename)s carregado com sucesso', filename=filename)})
        else:
            return jsonify({'error': _('Tipo de arquivo não suportado')}), 400
            
    except Exception as e:
        logger.error(f"❌ Erro no upload: {e}")
        return jsonify({'error': str(e)}), 500

# -------------------------------
# Context Processor — info do usuário (CORRIGIDO)
# -------------------------------
@app.context_processor
def inject_user_components():
    """Injeta informações do usuário nos templates"""
    user_id = session.get('user_id')
    username = ''
    location_name = ''
    location_id = None               # <-- ADICIONAR
    user_menus = []
    user_component_names = []
    current_language = get_locale()

    if user_id:
        user = User.query.get(user_id)
        if user:
            username = getattr(user, 'fullname', user.username)
            location_name = getattr(user.location, 'name', '') if getattr(user, 'location', None) else ''
            location_id = getattr(user, 'location_id', None)   # <-- ADICIONAR
            componentes = UserComponente.query.filter_by(user_id=user_id).all()
            user_component_names = [uc.componente.descricao for uc in componentes if uc.componente]
            user_menus = get_user_menus(user_id)
            
            # Log para debug
            logger.info(f"Usuário {username} (ID: {user_id})")
            logger.info(f"Componentes atribuídos: {user_component_names}")
            logger.info(f"Menus ativados: {user_menus}")
            
            # Verifica se usuário tem idioma preferencial salvo
            if hasattr(user, 'language') and user.language:
                current_language = user.language

    return dict(
        username=username,
        location_name=location_name,
        location_id=location_id,      # <-- ADICIONAR
        user_components=user_component_names,
        user_menus=user_menus,
        current_year=datetime.now().year,
        current_language=current_language,
        language_flag=get_language_flag(current_language)
    )

@app.route('/api/debug/user-menus', methods=['GET'])
def debug_user_menus():
    """Endpoint para debug dos menus do usuário"""
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    componentes = UserComponente.query.filter_by(user_id=user_id).all()
    user_component_names = [uc.componente.descricao for uc in componentes if uc.componente]
    user_menus = get_user_menus(user_id)
    
    return jsonify({
        'user_id': user_id,
        'username': user.username,
        'components': user_component_names,
        'menus': user_menus,
        'all_possible_menus': [
            'locationMenu',
            'registoMenu',
            'alosaudeMenu',
            'testagemMenu',
            'mappingMenu',
            'gestaoAlocacaoMenu',
            'gestaoFormacaoMenu',
            'trackingMenu',
            'DODtrackingMenu',
            'rhMenu',
            'userMenu'
        ]
    })

def get_language_flag(lang):
    """Retorna emoji da bandeira para o idioma"""
    flags = {
        'pt': '🇵🇹',  # Português
        'en': '🇺🇸',  # Inglês
        'es': '🇪🇸',  # Espanhol
        'fr': '🇫🇷',  # Francês
    }
    return flags.get(lang, '🌐')

# -------------------------------
# ROTAS FRONTEND
# -------------------------------
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
                         system_activity=_('Online'))

@app.route('/content/<page>')
def content(page):
    # Converter para minúsculas
    page = page.lower()
    
    # Verificar autenticação
    if 'user_id' not in session:
        flash(_('Por favor, faça login primeiro.'), 'warning')
        return redirect(url_for('login'))
    
    # Páginas básicas sempre permitidas
    if page in ['dashboard', 'dashboarddistribuicao', 'dashboarddoddistribuicao', 'pisaudedashboard']:
        try:
            return render_template(f'{page}.html')
        except Exception as e:
            logger.error(f"Erro ao carregar template '{page}.html': {str(e)}")
            flash(_('Erro ao carregar a página %(page)s', page=page), 'danger')
            return redirect(url_for('dashboard'))
    
    # Verificar se a página é permitida para o usuário
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if user:
        # Buscar menus permitidos para o usuário
        user_menus = get_user_menus(user_id)
        
        # Mapeamento de páginas para menus principais
        page_to_menu = {
            # (mantenha seus mapeamentos aqui)
        }
        
        # Verificar se a página é permitida
        if page in page_to_menu:
            required_menu = page_to_menu[page]
            
            # Verificar se o usuário tem o menu necessário
            if required_menu not in user_menus:
                flash(_('Você não tem permissão para acessar esta página.'), 'danger')
                return redirect(url_for('dashboard'))
    
    try:
        return render_template(f'{page}.html')
    except Exception as e:
        logger.error(f"Erro ao carregar template '{page}.html': {str(e)}")
        flash(_('Erro ao carregar a página %(page)s', page=page), 'danger')
        return redirect(url_for('dashboard'))

# -------------------------------
# LOGIN / LOGOUT
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # login_user(user)   # 👈 ESSENCIAL
            session['user_id'] = user.id
            session['username'] = user.username
            session['location_name'] = user.location.name if user.location else ''
            
            
            # Define idioma da sessão baseado no usuário
            if hasattr(user, 'language') and user.language:
                session['lang'] = user.language
            
            flash(_('Login efetuado com sucesso!'), 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(_('Usuário ou senha inválidos.'), 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash(_('Sessão terminada com sucesso.'), 'info')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

# -------------------------------
# ROTAS PÚBLICAS - REGISTRO DE USUÁRIO
# -------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página pública de registro de novos usuários"""
    # Se usuário já estiver logado, redireciona para dashboard
    if 'user_id' in session:
        flash(_('Você já está logado!'), 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            # Coletar dados do formulário
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            fullname = request.form.get('fullname')
            email = request.form.get('email')
            
            # Validações básicas
            if not username or not password or not fullname:
                flash(_('Por favor, preencha todos os campos obrigatórios.'), 'danger')
                return render_template('register.html')
            
            if password != confirm_password:
                flash(_('As senhas não coincidem.'), 'danger')
                return render_template('register.html')
            
            # Verificar se usuário já existe
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash(_('Nome de usuário já está em uso.'), 'danger')
                return render_template('register.html')
            
            # Hash da senha
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash(password)
            
            # Criar novo usuário
            new_user = User(
                username=username,
                password=hashed_password,
                fullname=fullname,
                email=email if email else None,
                language='pt',  # Idioma padrão
                is_active=True,
                created_at=datetime.now(),
                # Você pode adicionar outros campos padrão aqui
                location_id=1,  # Se houver uma localização padrão
                role_id=1,      # Se houver uma função padrão
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash(_('Conta criada com sucesso! Faça login para continuar.'), 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            flash(_('Ocorreu um erro ao criar sua conta. Tente novamente.'), 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

# -------------------------------
# FUNÇÕES AUXILIARES
# -------------------------------
def get_user_menus(user_id):
    """Retorna lista de IDs de menus permitidos para o usuário"""
    user_menus = []
    componentes = UserComponente.query.filter_by(user_id=user_id).all()
    user_component_names = [uc.componente.descricao.strip().lower() for uc in componentes if uc.componente]
    
    # Mapeamento mais completo e consistente
    componente_to_menu = {
        # Componentes e seus respectivos menus
        'formação': 'gestaoFormacaoMenu',
        'mapeamento de recursos': 'mappingMenu', 
        'afetação / alocação': 'gestaoAlocacaoMenu',
        'itens tracking': 'trackingMenu',
        'alo-saúde': 'alosaudeMenu',
        'menu de registos': 'registoMenu',
        'menu de recursos humanos': 'rhMenu',
        'menus do usuário': 'userMenu',
        'menus de localização': 'locationMenu',
        'menus de grupos de alo saúde': 'gruposAlosaudeMenus',
        'módulo alo-saúde': 'moduloAloSaude',
        
        # Adicione mais mapeamentos conforme necessário
        'gestão de localizações': 'locationMenu',
        'localização': 'locationMenu',
        'gestão de usuários': 'userMenu',
        'recursos humanos': 'rhMenu',
        'registos': 'registoMenu',
        'testagem': 'testagemMenu',  # Se existir este componente
    }
    
    for component_name in user_component_names:
        # Tenta encontrar correspondência exata primeiro
        if component_name in componente_to_menu:
            menu_id = componente_to_menu[component_name]
            if menu_id not in user_menus:
                user_menus.append(menu_id)
        else:
            # Tenta correspondência parcial
            for key, value in componente_to_menu.items():
                if key in component_name or component_name in key:
                    if value not in user_menus:
                        user_menus.append(value)
                    break
    
    # Log para debug
    logger.debug(f"User {user_id} components: {user_component_names}")
    logger.debug(f"User {user_id} menus: {user_menus}")
    
    return user_menus

# -------------------------------
# ROTA DE IMPORTAÇÃO DE OBSERVAÇÕES
# -------------------------------
@app.route('/api/observations/import', methods=['POST'])
def import_observations():
    if not request.is_json:
        return jsonify({'error': _('Content-Type deve ser application/json')}), 415
        
    data = request.get_json()
    if not data:
        return jsonify({'error': _('JSON inválido ou payload vazio')}), 400

    stateId = data.get("stateID")
    groupTypeId = data.get("groupTypeID")
    grupoPacientes = data.get("grupoPacientes")
    observations = data.get("observations", [])

    # Dados do usuário logado
    # location_id = current_user.location_id
    # user_id = current_user.id

    # Dados do usuário logado
    print(f"DEBUG: current_user = {current_user}")
    print(f"DEBUG: current_user.id = {getattr(current_user, 'id', None)}")
    print(f"DEBUG: current_user.locationId = {getattr(current_user, 'locationId', None)}")

    location_id = getattr(current_user, 'locationId', None)
    if not location_id:
        # Log adicional para entender por que falhou
        print(f"ERRO: location_id não encontrado. current_user: {current_user}, atributos: {dir(current_user)}")
        return jsonify({'error': 'Usuário não possui localidade associada.'}), 403

    user_id = current_user.id
    print(f"DEBUG: location_id = {location_id}, user_id = {user_id}")

    batch, imported_count, errors = [], 0, []
    BATCH_SIZE = 50

    # Função para converter string para data
    def parse_date(date_str):
        if not date_str:
            return None
        
        try:
            if date_str is None or str(date_str).strip() == '':
                return None
            
            date_str = str(date_str).strip()
            
            if date_str == '' or date_str.lower() in ['null', 'none', 'nan', 'na']:
                return None
            
            # Tentar como número serial do Excel
            try:
                excel_serial = float(date_str)
                if 0 <= excel_serial < 100000:  # Aceita 0 também
                    base_date = datetime(1899, 12, 30)
                    result = base_date + timedelta(days=excel_serial)
                    print(f"DEBUG: Convertido número serial {excel_serial} para {result}")
                    return result
            except (ValueError, TypeError):
                pass
            
            # Remover timezone e microsegundos se existirem
            date_str_clean = re.sub(r'\.\d+', '', date_str)  # Remove microsegundos
            date_str_clean = re.sub(r'[+-]\d{2}:?\d{2}$', '', date_str_clean)  # Remove timezone
            
            # Lista de formatos de data
            date_formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%d-%m-%Y',
                '%m/%d/%Y',
                '%m/%d/%y',
                '%d/%m/%y',
                '%d.%m.%Y',
                '%Y/%m/%d',
                '%Y%m%d',
                '%d %b %Y',  # 15 Mar 2024
                '%d %B %Y',  # 15 March 2024
                '%b %d, %Y', # Mar 15, 2024
                '%B %d, %Y', # March 15, 2024
                '%d/%m/%Y %H:%M',
                '%d/%m/%Y %H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
            ]
            
            for fmt in date_formats:
                try:
                    result = datetime.strptime(date_str_clean.strip(), fmt)
                    print(f"DEBUG: Parseado '{date_str}' com formato {fmt}: {result}")
                    return result
                except ValueError:
                    continue
            
            print(f"AVISO: Formato de data não reconhecido: '{date_str}'")
            return None
            
        except Exception as e:
            print(f"ERRO ao converter data '{date_str}': {str(e)}")
            return None

    # Função para converter valor numérico para float
    def parse_numeric_value(val):
        try:
            if val is None or val == '':
                return 0
            
            # Se já for número
            if isinstance(val, (int, float)):
                return float(val)
            
            val_str = str(val).strip()
            
            # Se for string vazia
            if val_str == '' or val_str.lower() == 'null' or val_str.lower() == 'none':
                return 0
            
            # Remove espaços, R$, $, etc
            val_str = val_str.replace('R$', '').replace('$', '').replace('€', '').strip()
            
            # Remove espaços em branco entre números (ex: "101 000")
            val_str = val_str.replace(' ', '')
            
            # Verifica se tem separador de milhar e decimal
            if ',' in val_str and '.' in val_str:
                # Formato: 1.234,56 (ponto é milhar, vírgula é decimal)
                val_str = val_str.replace('.', '').replace(',', '.')
            elif ',' in val_str:
                # Formato: 1234,56 (vírgula é decimal)
                val_str = val_str.replace(',', '.')
            
            # Remove todos os caracteres não numéricos exceto ponto e negativo
            val_clean = ''.join(c for c in val_str if c.isdigit() or c == '.' or c == '-')
            
            if not val_clean or val_clean == '-':
                return 0
            
            result = float(val_clean)
            return result
            
        except Exception as e:
            print(f"Erro ao converter valor: {val} - {str(e)}")
            return 0

    for idx, row in enumerate(observations):
        try:
            # Debug: mostrar dados da linha
            print(f"\n=== Processando linha {idx} ===")
            print(f"Dados: {row}")
            
            # Extrair e converter datas importantes
            data_primeiro_carga_raw = row.get('data_primeiro_carga') or row.get('dataprimeiracv')
            data_ultima_carga_raw = row.get('data_ultima_carga') or row.get('dataultimacv')
            
            print(f"data_primeiro_carga (raw): {data_primeiro_carga_raw}")
            print(f"data_ultima_carga (raw): {data_ultima_carga_raw}")
            
            # Converter datas
            data_primeiro_carga = parse_date(data_primeiro_carga_raw)
            data_ultima_carga = parse_date(data_ultima_carga_raw)
            
            print(f"data_primeiro_carga (converted): {data_primeiro_carga}")
            print(f"data_ultima_carga (converted): {data_ultima_carga}")
            
            # Converter outras datas
            data_inicio = parse_date(row.get('data_inicio'))
            data_seguimento = parse_date(row.get('data_seguimento'))
            
            obs = Observation(
                nid=str(row.get('NID', '') or row.get('nid', '')).strip(),
                fullname=str(row.get('NomeCompleto', '') or row.get('Nome', '') or row.get('fullname', '')).strip(),
                gender=str(row.get('gender', '')).strip().upper()[:1],
                age=int(parse_numeric_value(row.get('idade_actual') or row.get('age') or row.get('idade') or 0)),
                contact=str(row.get('Telefone', '') or row.get('contact', '') or row.get('telefone', '')).strip(),
                occupation='',
                
                # DATAS IMPORTADAS DA PLANILHA
                datainiciotarv=data_inicio or datetime.now(),
                datalevantamento=data_seguimento or datetime.now(),
                dataproximolevantamento=datetime.now(),
                dataconsulta=datetime.now(),
                dataproximaconsulta=datetime.now(),
                dataalocacao=datetime.now(),
                dataenvio=datetime.now(),
                
                smssendernumber='',
                smssuporternumber='',
                
                # CV - IMPORTADOS DA PLANILHA
                dataprimeiracv=data_primeiro_carga,
                valorprimeiracv=parse_numeric_value(row.get('valor_primeira_carga') or row.get('valorprimeiracv')),
                dataultimacv=data_ultima_carga,  # Pode ser None
                valorultimacv=parse_numeric_value(row.get('valor_ultima_carga') or row.get('valorultimacv')),
                
                linhaterapeutica='',
                regime='',
                status='',
                
                stateId=stateId,
                textmessageId=1,
                grouptypeId=groupTypeId,
                groupId=1,
                locationId=location_id,
                userId=user_id,
            )
            batch.append(obs)
            imported_count += 1
            
            if len(batch) >= BATCH_SIZE:
                db.session.add_all(batch)
                db.session.flush()
                batch = []
                
        except Exception as e:
            errors.append({'row': idx, 'error': str(e), 'data': row})
            print(f"Erro na linha {idx}: {str(e)}")

    if batch:
        db.session.add_all(batch)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': _('Falha no commit do banco de dados'), 'details': str(e)}), 500

    return jsonify({
        'message': _('Importação concluída'),
        'imported_count': imported_count,
        'errors': errors
    }), 200

# -------------------------------
# MANIPULADORES DE ERRO (CORRIGIDOS)
# -------------------------------
@app.errorhandler(404)
def not_found_error(error):
    """Manipulador de erro 404"""
    # Usar HTML inline em vez de template para evitar problemas
    return """
    <!DOCTYPE html>
    <html lang="pt">
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
    """Manipulador de erro 500"""
    db.session.rollback()
    logger.error(f"Erro interno do servidor: {error}")
    
    # Usar HTML inline em vez de template para evitar problemas
    return """
    <!DOCTYPE html>
    <html lang="pt">
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
# INICIALIZAÇÃO DA APLICAÇÃO
# -------------------------------
if __name__ == '__main__':
    logger.info("🚀 Iniciando aplicação PI-SAÚDE com Jhpiego Bot e sistema de idiomas...")
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host="0.0.0.0", port=5000)