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

# -------------------------------
# CONFIGURAÇÃO DO BABEL (IDIOMAS)
# -------------------------------
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en', 'es', 'fr']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

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
from routes.MedicamentoRoutes import medicamento_bp
from routes.HistoricoMovimentoRoutes import historico_movimento_bp
from routes.StockSemanalRoutes import stock_semanal_bp
from routes.StockSemanalLoteRoutes import stock_semanal_lote_bp
from routes.DashboardMedicamentoRoutes import dashboard_bp

# Route exclusiva para o Bot
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
    items_solicitados_bp, agendamento_bp, medicamento_bp, historico_movimento_bp,
    stock_semanal_bp, stock_semanal_lote_bp, dashboard_bp, ai_bp
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
    user_menus = []
    user_component_names = []
    current_language = get_locale()

    if user_id:
        user = User.query.get(user_id)
        if user:
            username = getattr(user, 'fullname', user.username)
            location_name = getattr(user.location, 'name', '') if getattr(user, 'location', None) else ''
            componentes = UserComponente.query.filter_by(user_id=user_id).all()
            user_component_names = [uc.componente.descricao for uc in componentes if uc.componente]
            user_menus = get_user_menus(user_id)
            
            # Verifica se usuário tem idioma preferencial salvo
            if hasattr(user, 'language') and user.language:
                current_language = user.language

    return dict(
        username=username,
        location_name=location_name,
        user_components=user_component_names,
        user_menus=user_menus,
        current_year=datetime.now().year,
        current_language=current_language,
        language_flag=get_language_flag(current_language)
    )

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
# FUNÇÕES AUXILIARES
# -------------------------------
def get_user_menus(user_id):
    user_menus = []
    componentes = UserComponente.query.filter_by(user_id=user_id).all()
    user_component_names = [uc.componente.descricao for uc in componentes if uc.componente]
    
    # Log para depuração
    logger.info(f"Componentes do usuário {user_id}: {user_component_names}")
    
    componente_to_menu = {
        'Formação': 'gestaoFormacaoMenu',
        'Mapeamento de recursos': 'mappingMenu', 
        'Afetação / Alocação': 'gestaoAlocacaoMenu',
        'Itens Traking': 'trackingMenu',
        'DOD Tracking': 'DODtrackingMenu',
        'Alo-Saúde': 'alosaudeMenu',
        'Menu de registos': 'registoMenu',
        'Menu de Recursos Humanos': 'rhMenu',
        'Menus do usuário': 'userMenu',
        'Gestão de Localizações': 'locationMenu',
        'Menus de grupos de alo saúde': 'gruposAlosaudeMenus',
        'Módulo Alo-Saúde': 'moduloAloSaude',
        'Agendar de consultas':'agendarConsultaMenu',
        'Gestão de Farmácia': 'farmaciaMenu',
        'Manus do usuário':'userMenus',
    }
    
    for component_name in user_component_names:
        if component_name in componente_to_menu:
            user_menus.append(componente_to_menu[component_name])
    
    logger.info(f"Menus gerados para o usuário {user_id}: {user_menus}")
    return user_menus

# -------------------------------
# ROTA DE IMPORTAÇÃO DE OBSERVAÇÕES
# -------------------------------
@app.route('/api/observations/import', methods=['POST'])
def import_observations():
 # Verificar autenticação
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    # Buscar usuário no banco
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 401

    # Obter locationId do usuário (supondo que user.location_id exista)
    location_id = user.locationId  # ou user.locationId, conforme seu modelo
    if not location_id:
        return jsonify({'error': 'Usuário não possui localidade associada'}), 403

    # Validações do payload
    if not request.is_json:
        return jsonify({'error': _('Content-Type deve ser application/json')}), 415
        
    data = request.get_json()
    if not data:
        return jsonify({'error': _('JSON inválido ou payload vazio')}), 400

    stateId = data.get("stateID")
    grouptypeId = data.get("groupTypeID")
    textmessageId = data.get("selectTextMessage")
    # grupoPacientes = data.get("grupoPacientes")
    observations = data.get("observations", [])

    batch, imported_count, errors = [], 0, []
    BATCH_SIZE = 50

    # Função para converter string para data
    def parse_date(date_str):
        if not date_str:
            return None
            
        try:
            # Se for None ou string vazia
            if date_str is None or str(date_str).strip() == '':
                return None
            
            date_str = str(date_str).strip()
            
            # Se for string vazia após strip
            if date_str == '' or date_str.lower() == 'null' or date_str.lower() == 'none':
                return None
            
            # DEBUG: Mostrar o que está sendo processado
            print(f"DEBUG parse_date input: '{date_str}'")
            
            # PRIMEIRO: Verificar se é um número serial do Excel
            # Números serial do Excel geralmente são > 40000 para datas recentes
            try:
                # Tenta converter para float
                excel_serial = float(date_str)
                # Se for um número razoável para data do Excel (entre 0 e 100000)
                if 0 < excel_serial < 100000:
                    print(f"DEBUG: Detectado número serial do Excel: {excel_serial}")
                    # Converter número serial do Excel para data
                    # Excel base date is 1899-12-30 for Windows
                    base_date = datetime(1899, 12, 30)
                    result = base_date + timedelta(days=excel_serial)
                    print(f"DEBUG: Convertido para: {result}")
                    return result
            except (ValueError, TypeError):
                pass  # Não é um número, continua com o parsing normal
            
            # SEGUNDO: Tentar remover "T00:00" e " 0:00" do final
            date_str_clean = date_str.replace('T00:00', '').replace(' 0:00', '').strip()
            
            # Lista de formatos de data a tentar
            date_formats = [
                '%Y-%m-%d',        # 2024-03-15
                '%d/%m/%Y',        # 15/03/2024
                '%d-%m-%Y',        # 15-03-2024
                '%m/%d/%Y',        # 03/15/2024 (formato americano)
                '%m/%d/%y',        # 03/15/24 (formato americano curto)
                '%d/%m/%y',        # 15/03/24
                '%d.%m.%Y',        # 15.03.2024
                '%Y/%m/%d',        # 2024/03/15
                '%Y%m%d',          # 20240315
            ]
            
            for fmt in date_formats:
                try:
                    result = datetime.strptime(date_str_clean, fmt)
                    print(f"DEBUG: Parseado com formato {fmt}: {result}")
                    return result
                except ValueError:
                    continue
            
            print(f"DEBUG: Formato de data não reconhecido: '{date_str}'")
            return None
            
        except Exception as e:
            print(f"Erro ao converter data: {date_str} - {str(e)}")
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

            # --- Campos normalizados vs originais ---
            nid_val = row.get('NID') or row.get('nid') or ''
            fullname_val = row.get('NomeCompleto') or row.get('fullname') or row.get('Nome') or ''
            gender_val = row.get('gender') or row.get('Gender') or ''
            age_val = row.get('idade_actual') or row.get('age') or row.get('Idade') or 0
            contact_val = row.get('Telefone') or row.get('contact') or row.get('telefone') or ''

            # Datas de carga viral
            data_primeiro_carga_raw = row.get('data_primeiro_carga') or row.get('dataprimeiracv')
            data_ultima_carga_raw = row.get('data_ultima_carga') or row.get('dataultimacv')
            # Valores de carga viral
            valor_primeira_carga_raw = row.get('valor_primeira_carga') or row.get('valorprimeiracv')
            valor_ultima_carga_raw = row.get('valor_ultima_carga') or row.get('valorultimacv')

            # Outras datas
            data_inicio_raw = row.get('data_inicio')
            data_seguimento_raw = row.get('data_seguimento')

            # --- stateId individual (prioritário) ---
            obs_state_id = row.get('stateId')
            if obs_state_id is None:
                obs_state_id = stateId   # valor geral do payload

            # Converter datas
            data_primeiro_carga = parse_date(data_primeiro_carga_raw)
            data_ultima_carga = parse_date(data_ultima_carga_raw)
            data_inicio = parse_date(data_inicio_raw)
            data_seguimento = parse_date(data_seguimento_raw)

            obs = Observation(
                nid=str(nid_val).strip(),
                fullname=str(fullname_val).strip(),
                gender=str(gender_val).strip().upper()[:1],
                age=int(parse_numeric_value(age_val)),
                contact=str(contact_val).strip(),
                occupation='',
                
                datainiciotarv=data_inicio or datetime.now(),
                datalevantamento=data_seguimento or datetime.now(),
                dataproximolevantamento=datetime.now(),
                dataconsulta=datetime.now(),
                dataproximaconsulta=datetime.now(),
                dataalocacao=datetime.now(),
                dataenvio=datetime.now(),
                
                smssendernumber='',
                smssuporternumber='',
                
                dataprimeiracv=data_primeiro_carga,
                valorprimeiracv=parse_numeric_value(valor_primeira_carga_raw),
                dataultimacv=data_ultima_carga,
                valorultimacv=parse_numeric_value(valor_ultima_carga_raw),
                
                linhaterapeutica='',
                regime='',
                status='',
                smsStatus='',
                
                stateId=obs_state_id,   # usa o individual se existir
                textmessageId=textmessageId,
                grouptypeId=grouptypeId,
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