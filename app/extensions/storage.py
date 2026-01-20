from supabase import create_client
from flask import current_app

def get_supabase_client():
    '''
    Initialize Supabase using Flask app.config and returns client object
    '''
    
    url = current_app.config["SUPABASE_URL"]
    key = current_app.config["SUPABASE_KEY"]
    return create_client(url, key)
