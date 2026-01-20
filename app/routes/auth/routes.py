from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user
from mongoengine.errors import NotUniqueError, ValidationError
from app.config.roles import Roles
from . import auth_bp
from app.models.user import User
from werkzeug.security import generate_password_hash

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        user = User.objects(email=email).first()
        print(user.check_password(password))

        if not user:
            return render_template(
                "auth/login.html",
                error="User does not exist"
            )
        if not user.check_password(password):
            return render_template(
                "auth/login.html",
                error="Invalid email or password"
            )

        login_user(user)
        return redirect(url_for("auth.post_login"))  # change later

    return render_template("auth/login.html")

@auth_bp.route("/post-login")
def post_login():
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


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")
        role = request.form.get("role")
        # Basic validation
        if not email or not password or not role:
            return render_template(
                "auth/register.html",
                error="All fields are required"
            )

        try:
            user = User(
                email=email,
                role=role
            )
            user.set_password(password)
            user.save()

            return redirect(url_for("auth.login"))  # create later

        except NotUniqueError:
            return render_template(
                "auth/register.html",
                error="Email already registered"
            )

        except ValidationError as e:
            return render_template(
                "auth/register.html",
                error=str(e)
            )

        except Exception as e:
            return render_template(
                "auth/register.html",
                error=f"{e}"
            )

    return render_template("auth/register.html")


