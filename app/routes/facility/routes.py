from flask import render_template
from flask_login import login_required

from . import facility_bp
from app.decorators import role_required
from app.config.roles import Roles


@facility_bp.route("/dashboard")
@login_required
@role_required(Roles.FACILITY)
def dashboard():
    return render_template("facility/dashboard.html")


@facility_bp.route("/generate")
@login_required
@role_required(Roles.FACILITY)
def generate():
    return render_template("facility/generate.html")
