from flask import render_template
from flask_login import login_required

from . import civic_bp
from app.decorators import role_required
from app.config.roles import Roles


@civic_bp.route("/dashboard")
@login_required
@role_required(Roles.CIVIC)
def dashboard():
    return render_template("civic/dashboard.html")
