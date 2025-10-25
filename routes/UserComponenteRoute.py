from flask import Blueprint
from controllers.UserComponenteController import UserComponenteController

usercomponente_bp = Blueprint('usercomponente', __name__)

# Rotas principais
usercomponente_bp.route('/usercomponente', methods=['POST'])(UserComponenteController.create)
usercomponente_bp.route('/usercomponente', methods=['GET'])(UserComponenteController.get_user_componentes)
usercomponente_bp.route('/usercomponente/<int:id>', methods=['GET'])(UserComponenteController.get_by_id)
usercomponente_bp.route('/usercomponente/<int:id>', methods=['PUT'])(UserComponenteController.update)
usercomponente_bp.route('/usercomponente/<int:id>', methods=['DELETE'])(UserComponenteController.delete)

# Exemplo de rotas adicionais, se necessário
# usercomponente_bp.route('/users/<int:user_id>/componentes', methods=['GET'])(UserComponenteController.get_user_componentes)
# usercomponente_bp.route('/componentes/<int:componente_id>/users', methods=['GET'])(UserComponenteController.get_componente_users)
