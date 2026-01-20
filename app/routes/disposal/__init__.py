from flask import Blueprint

disposal_bp = Blueprint("disposal", __name__, url_prefix="/disposal")

from . import routes
