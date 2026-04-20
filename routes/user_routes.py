from flask import Blueprint, jsonify, request
from models.user import User
from database import db
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt

user_bp = Blueprint('user', __name__)

@user_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})

    return jsonify({'message': 'Invalid data'}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'message': 'Login successful'})

    return jsonify({'message': 'Invalid username or password'}), 401

@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if user_id != current_user.id and current_user.role == 'user':
        return jsonify({'message': 'You cannot update this user'}), 403
    
    if user and data.get("password"):
        user.password = bcrypt.hashpw(str.encode(data['password']), bcrypt.gensalt())
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
  
    return jsonify({'message': f'User {user_id} not found'}), 404

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if current_user.role == 'user':
        return jsonify({'message': 'Operation not permitted'}), 403
    
    if user and user_id == current_user.id:
        return jsonify({'message': 'You cannot delete your own account'}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})

    return jsonify({'message': 'User not found'}), 404