from flask import render_template,request,redirect,url_for
from flask_login import login_required,current_user

from . import facility_bp
from app.decorators import role_required
from app.config.roles import Roles


@facility_bp.route("/dashboard")
@login_required
@role_required(Roles.FACILITY)
def dashboard():
    return render_template("facility/dashboard.html")


@facility_bp.route("/profile/setup", methods=["GET", "POST"])
@login_required
def profile_setup():

    # Safety: only facility users allowed
    if current_user.role != "facility":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        details = {
            "facility_name": request.form.get("facility_name"),
            "facility_type": request.form.get("facility_type"),
            "registration_id": request.form.get("registration_id"),
            "license_no": request.form.get("license_no"),
            "address": request.form.get("address"),
            "city": request.form.get("city"),
            "state": request.form.get("state"),
            "pincode": request.form.get("pincode"),
            "max_capacity": request.form.get("max_capacity"),
            "waste_categories": request.form.getlist("waste_categories"),
            "approved": False  # civic approval later
        }

        current_user.details = details
        current_user.save()

        return redirect(url_for("facility.dashboard"))

    return render_template("facility/profile_setup.html")

