from flask import Flask, render_template  # type: ignore
from models import db
from config import Config

# Importações das rotas (blueprints)
from routes.ContactLinkRoutes import contactlink_bp
from routes.ObservationRoutes import observation_bp
from routes.DailyRecordRoutes import dailyrecord_bp
from routes.LocationRoutes import location_bp
from routes.RoleRoutes import role_bp
from routes.GroupRoutes import group_bp
from routes.GrouptyeRoutes import grouptype_bp
from routes.StateRoutes import state_bp
from routes.TextmessageRoute import textmessage_bp
from routes.UserRoleRoutes import user_role_bp
from routes.UserRoutes import user_bp
from routes.KeyPopulationRoutes import keypopulation_bp
from routes.PortaTestagemRoutes import portatestagem_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Registro dos blueprints com prefixo "/api"
app.register_blueprint(contactlink_bp, url_prefix='/api') 
app.register_blueprint(dailyrecord_bp, url_prefix='/api')
app.register_blueprint(observation_bp, url_prefix='/api')
app.register_blueprint(location_bp, url_prefix='/api')
app.register_blueprint(role_bp, url_prefix='/api')
app.register_blueprint(group_bp, url_prefix='/api')
app.register_blueprint(grouptype_bp, url_prefix='/api')
app.register_blueprint(state_bp, url_prefix='/api')
app.register_blueprint(textmessage_bp, url_prefix='/api')
app.register_blueprint(user_role_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(keypopulation_bp, url_prefix='/api')
app.register_blueprint(portatestagem_bp, url_prefix='/api')

# Rotas básicas para renderização de páginas
@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/content/<page>')
def content(page):
    return render_template(f'{page}')

# Inicialização da app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
