from flask import Flask
from flask_session import Session
from flask_login import current_user

from app.config.env import load_env
from app.config.settings import DevelopmentConfig
from app.extensions.database import init_db
from app.extensions.login_manager import login_manager
from zoneinfo import ZoneInfo  # Python 3.9+

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

    UTC = ZoneInfo("UTC")
    IST = ZoneInfo("Asia/Kolkata")
    def to_ist(dt):
        if not dt:
            return ""
        if dt.tzinfo is None:
            # Assume UTC if naive
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(IST)

    def datetime_format(value, format='%d/%m/%Y %I:%M %p'):
        if not value:
            return ""
        return value.strftime(format)

    app.jinja_env.filters['to_ist'] = to_ist
    app.jinja_env.filters['datetime_format'] = datetime_format


    return app
