import bcrypt
from flask import Flask, jsonify, request
from models.meals import Meal
from models.user import User
from database import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost/daily_diet_db'

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes.user_routes import user_bp
from routes.meal_routes import meal_bp

app.register_blueprint(user_bp)
app.register_blueprint(meal_bp)

if __name__ == '__main__':
    app.run(debug=True)
