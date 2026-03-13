from flask import Blueprint
from controllers.DashboardMedicamentoController import DashboardMedicamentoController

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/medicamento', methods=['GET'])
def get_dashboard_data():
    return DashboardMedicamentoController.get_dashboard_data()