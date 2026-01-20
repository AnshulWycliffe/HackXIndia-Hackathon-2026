from flask import Flask
from flask_session import Session

from app.config.env import load_env
from app.config.settings import DevelopmentConfig
from app.extensions.database import init_db
from app.extensions.login_manager import login_manager

def create_app():
    # Load environment variables
    load_env()

    app = Flask(__name__)

    # Load config object
    app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    init_db(app)
    Session(app)
    
    login_manager.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.civic import civic_bp
    from app.routes.facility import facility_bp
    from app.routes.collector import collector_bp
    from app.routes.disposal import disposal_bp
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(civic_bp)
    app.register_blueprint(facility_bp)
    app.register_blueprint(collector_bp)
    app.register_blueprint(disposal_bp)

    return app
