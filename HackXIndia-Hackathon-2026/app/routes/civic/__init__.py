from flask import Blueprint

civic_bp = Blueprint("civic", __name__, url_prefix="/civic")

from . import routes
