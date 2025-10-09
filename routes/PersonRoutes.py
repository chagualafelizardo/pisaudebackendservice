from flask import Blueprint
from controllers.PersonController import PersonController

person_bp = Blueprint('person', __name__)

# GET all persons
@person_bp.route('/person', methods=['GET'])
def get_persons():
    return PersonController.get_all()

# GET person by ID
@person_bp.route('/person/<int:id>', methods=['GET'])
def get_person(id):
    return PersonController.get_by_id(id)

# POST create new person
@person_bp.route('/person', methods=['POST'])
def create_person():
    return PersonController.create()

# PUT update existing person
@person_bp.route('/person/<int:id>', methods=['PUT'])
def update_person(id):
    return PersonController.update(id)

# DELETE remove person
@person_bp.route('/person/<int:id>', methods=['DELETE'])
def delete_person(id):
    return PersonController.delete(id)
