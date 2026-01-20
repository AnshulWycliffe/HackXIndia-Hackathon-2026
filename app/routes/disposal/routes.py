from flask import render_template
from flask_login import login_required

from . import disposal_bp
from app.decorators import role_required
from app.config.roles import Roles


@disposal_bp.route("/dashboard")
@login_required
@role_required(Roles.DISPOSAL)
def dashboard():
    return render_template("disposal/dashboard.html")
