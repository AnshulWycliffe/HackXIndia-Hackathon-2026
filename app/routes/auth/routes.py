from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from . import auth_bp
from app.models.user import User

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.objects(email=email).first()

        if not user or not user.verify_password(password):
            flash("Invalid credentials", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("auth.post_login"))

    return render_template("auth/login.html")

@auth_bp.route("/post-login")
def post_login():
    from app.config.roles import Roles
    from flask_login import current_user

    if current_user.role == Roles.CIVIC:
        return redirect(url_for("civic.dashboard"))

    if current_user.role == Roles.FACILITY:
        return redirect(url_for("facility.dashboard"))

    if current_user.role == Roles.COLLECTOR:
        return redirect(url_for("collector.dashboard"))

    if current_user.role == Roles.DISPOSAL:
        return redirect(url_for("disposal.dashboard"))

    return redirect(url_for("public.home"))
