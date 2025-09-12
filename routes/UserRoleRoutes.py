from flask import Blueprint
from controllers.UserRoleController import UserRoleController

userrole_bp = Blueprint('userrole', __name__)

userrole_bp.route('/userrole', methods=['POST'])(UserRoleController.create)
userrole_bp.route('/userrole', methods=['GET'])(UserRoleController.get_all)
userrole_bp.route('/userrole/<int:id>', methods=['DELETE'])(UserRoleController.delete)
# userrole_bp.route('/users/<int:userId>/roles', methods=['GET'])(UserRoleController.get_user_roles)
# userrole_bp.route('/roles/<int:roleId>/users', methods=['GET'])(UserRoleController.get_users_by_role)
