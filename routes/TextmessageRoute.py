from flask import Blueprint
from controllers.TextmessageController import TextmessageController

textmessage_bp = Blueprint('textmessage', __name__)

@textmessage_bp.route('/textmessage', methods=['GET'])
def get_textmessages():
    return TextmessageController.get_all()

@textmessage_bp.route('/textmessage/<int:id>', methods=['GET'])
def get_textmessage(id):
    return TextmessageController.get_by_id(id)

@textmessage_bp.route('/textmessage', methods=['POST'])
def create_textmessage():
    return TextmessageController.create()

@textmessage_bp.route('/textmessage/<int:id>', methods=['PUT'])
def update_textmessage(id):
    return TextmessageController.update(id)

@textmessage_bp.route('/textmessage/<int:id>', methods=['DELETE'])
def delete_textmessage(id):
    return TextmessageController.delete(id)
