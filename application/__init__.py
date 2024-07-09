from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from flask_migrate import Migrate
from flask_login import current_user

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    db.init_app(app)
    migrate.init_app(app, db)


     # Register blueprints after database creation
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Listing

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if id is not None:
            return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('application/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')

if __name__ == '__main__':
    #app = create_app()
    app.run(debug=True)
