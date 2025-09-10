from flask import Blueprint
from controllers.ContactLinkController import ContactLinkController

contactlink_bp = Blueprint('contact_link', __name__)

@contactlink_bp.route('/contactlink', methods=['GET'])
def get_all_contact_links():
    return ContactLinkController.get_all()

@contactlink_bp.route('/contactlink/<int:id>', methods=['GET'])
def get_contact_link(id):
    return ContactLinkController.get_by_id(id)

@contactlink_bp.route('/contactlink', methods=['POST'])
def create_contact_link():
    return ContactLinkController.create()

@contactlink_bp.route('/contactlink/<int:id>', methods=['DELETE'])
def delete_contact_link(id):
    return ContactLinkController.delete(id)
