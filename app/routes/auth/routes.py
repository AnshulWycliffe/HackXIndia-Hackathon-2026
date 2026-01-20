from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user
from app.extensions.storage import get_supabase_client
from app.config.roles import Roles
from . import auth_bp
from app.models.user import User
from werkzeug.security import generate_password_hash

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


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Extract form data
        organization_name = request.form.get("organization_name")
        organization_type = request.form.get("organization_type")
        license_number = request.form.get("license_number")
        address = request.form.get("address")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        waste_categories = request.form.getlist("waste_categories")
        max_capacity = request.form.get("max_capacity_per_day")
        assigned_zone = request.form.get("assigned_zone")
        email = request.form.get("email")
        password = request.form.get("password")

        # Handle license file upload via Supabase
        license_file = request.files.get("license_document")
        supabase = get_supabase_client()
        license_path = None
        if license_file:
            file_name = f"licenses/{email}_{license_file.filename}"
            supabase.storage.from_(current_app.config["SUPABASE_BUCKET"]).upload(file_name, license_file.read())
            license_path = file_name

        # Create user object
        user = User(
            role=Roles.FACILITY,
            organization_name=organization_name,
            organization_type=organization_type,
            license_number=license_number,
            license_document=license_path,
            address=address,
            geo_location={"lat": lat, "lng": lng},
            waste_categories=waste_categories,
            max_capacity_per_day=max_capacity,
            assigned_zone=assigned_zone,
            email=email,
            password_hash=generate_password_hash(password),
            status="PENDING"
        )

        user.save()
        flash("Registration successful! Awaiting civic approval.", "success")
        return redirect(url_for("auth.register"))

    return render_template("auth/register.html")