from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

if __name__ == '__main__':
    from flask import Flask
    from models.user import User
    from models.meals import Meal

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost/daily_diet_db'
    db.init_app(app)

    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Models registered:", [cls.__name__ for cls in db.Model.__subclasses__()])
        print("Creating all tables...")
        db.create_all()
        print("Database reset and tables created.")