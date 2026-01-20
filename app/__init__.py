from flask import Flask, redirect, flash, request, url_for, g, render_template
from flask_session import Session  # For session management
from flask_login import LoginManager, current_user  # For user authentication

import atexit, shutil

import os


from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
# from pytz import timezone  # use this instead if < Python 3.9

def create_app():
        
    from dotenv import dotenv_values

    from app.service.database import init_db
    
    env = dotenv_values()

    app = Flask(__name__)

    app.secret_key = env["SECRET_KEY"]
    app.config['MONGO_URI'] = env['MONGO_URI']
    app.config['MONGO_DBNAME'] = env["MONGO_DBNAME"]
    app.config['MONGO_USERNAME'] = env['MONGO_USERNAME']
    app.config['MONGO_PASSWORD'] = env["MONGO_PASSWORD"]

    app.config["SUPABASE_KEY"] = env["SUPABASE_KEY"]
    app.config["SUPABASE_URL"] = env["SUPABASE_URL"]
    app.config["SUPABASE_BUCKET"] = env["SUPABASE_BUCKET"]

    app.config["SESSION_PERMANENT"] = False  # session ends when browser closes
    app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem for session storage
    app.config['SESSION_FILE_DIR'] = './flask_session'  # Use filesystem for session storage

    

    # Initialize MongoEngine
    init_db(app)


    return app
