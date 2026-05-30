from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models.models import db
from config.config import Config
import os

login_manager = LoginManager()
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    from models.models import User
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/mce_placement_db'

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from routes.auth_routes import auth_bp
    from routes.main_routes import main_bp
    from routes.resume_routes import resume_bp
    from routes.prediction_routes import prediction_bp
    from routes.admin_routes import admin_bp
    from routes.chatbot_routes import chatbot_bp
    from routes.recommendation_routes import recommend_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(resume_bp, url_prefix='/resume')
    app.register_blueprint(prediction_bp, url_prefix='/predict')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(recommend_bp, url_prefix='/recommendations')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        db.create_all()
        from utils.db_seeder import seed_admin
        seed_admin()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)