from flask import Blueprint

facility_bp = Blueprint("facility", __name__, url_prefix="/facility")

from . import routes
