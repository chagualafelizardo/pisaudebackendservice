from flask import Blueprint
from controllers.DailyRecordController import DailyRecordController

dailyrecord_bp = Blueprint('dailyrecord_bp', __name__)  # Sem underscore
# Rota para obter todos os registros
@dailyrecord_bp.route('/dailyrecord', methods=['GET'])
def get_all_daily_records():
    return DailyRecordController.get_all()

# Rota para obter um registro por ID
@dailyrecord_bp.route('/dailyrecord/<int:id>', methods=['GET'])
def get_daily_record_by_id(id):
    return DailyRecordController.get_by_id(id)

# Rota para criar um novo registro
@dailyrecord_bp.route('/dailyrecord', methods=['POST'])
def create_daily_record():
    return DailyRecordController.create()

# Rota para deletar um registro por ID
@dailyrecord_bp.route('/dailyrecord/<int:id>', methods=['DELETE'])
def delete_daily_record(id):
    return DailyRecordController.delete(id)
