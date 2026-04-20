from flask import Blueprint, jsonify, request
from models.meals import Meal
from database import db
from flask_login import login_required, current_user

meal_bp = Blueprint('meal', __name__)

@meal_bp.route('/meals', methods=['POST'])
@login_required
def create_meal():
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    good_for_diet = data.get('good_for_diet', True)

    if name:
        meal = Meal(name=name, description=description, date=date, good_for_diet=good_for_diet, user_id=current_user.id)
        db.session.add(meal)
        db.session.commit()
        return jsonify({'message': 'Meal created successfully'})
    
    return jsonify({'message': 'Invalid data'}), 400

@meal_bp.route('/meals', methods=['GET'])
@login_required
def get_meals():
    if current_user.role == 'admin':
        meals = Meal.query.all()
    else:
        meals = Meal.query.filter_by(user_id=current_user.id).all()
    meals_list = [{'id': meal.id, 'name': meal.name, 'description': meal.description, 'date': meal.date, 'good_for_diet': meal.good_for_diet} for meal in meals]
    return jsonify(meals_list)

@meal_bp.route('/meal/<int:meal_id>', methods=['GET'])
@login_required
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if meal and (meal.user_id == current_user.id or current_user.role == 'admin'):
        return jsonify({'id': meal.id, 'name': meal.name, 'description': meal.description, 'date': meal.date, 'good_for_diet': meal.good_for_diet})
    return jsonify({'message': 'Meal not found or access denied'}), 404

@meal_bp.route('/meal/<int:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    data = request.get_json()
    meal = Meal.query.get(meal_id)

    if meal and (meal.user_id == current_user.id or current_user.role == 'admin'):
        meal.name = data.get('name', meal.name)
        meal.description = data.get('description', meal.description)
        meal.date = data.get('date', meal.date)
        meal.good_for_diet = data.get('good_for_diet', meal.good_for_diet)
        
        db.session.commit()
        return jsonify({'message': 'Meal updated successfully'})
    
    return jsonify({'message': 'Meal not found or access denied'}), 404

@meal_bp.route('/meal/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)

    if meal and (meal.user_id == current_user.id or current_user.role == 'admin'):
        db.session.delete(meal)
        db.session.commit()
        return jsonify({'message': 'Meal deleted successfully'})

    return jsonify({'message': 'Meal not found'}), 404