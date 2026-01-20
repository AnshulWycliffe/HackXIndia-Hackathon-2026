from flask import render_template
from flask_login import login_required

from . import collector_bp
from app.decorators import role_required
from app.config.roles import Roles


@collector_bp.route("/dashboard")
@login_required
@role_required(Roles.COLLECTOR)
def dashboard():
    return render_template("collector/dashboard.html")
