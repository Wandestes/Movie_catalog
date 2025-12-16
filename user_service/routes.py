from flask import Blueprint, request, jsonify
import user_service.users_repository as user_repo
from user_service.validation import validate_user_data

# Creating the blueprint
users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users', methods=['POST'])
def add_user():
    """Endpoint to create a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    is_valid, error_msg = validate_user_data(data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
        
    user_id = user_repo.create_user(data)
    if user_id:
        return jsonify({"id": user_id, "message": "User created"}), 201
    return jsonify({"error": "Internal server error"}), 500

@users_bp.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint to get user details by ID."""
    user = user_repo.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Endpoint to delete a user."""
    success = user_repo.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404