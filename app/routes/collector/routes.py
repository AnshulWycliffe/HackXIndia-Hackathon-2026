from flask import render_template, url_for,redirect,request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from . import collector_bp
from app.decorators import role_required
from app.config.roles import Roles


from app.models.user import User


@collector_bp.route("/dashboard")
@login_required
@role_required(Roles.COLLECTOR)
def dashboard():
    return render_template("collector/dashboard.html")


@collector_bp.route("/profile/setup", methods=["GET", "POST"])
@login_required
def profile_setup():

    # Role guard
    if current_user.role != "collector":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        details = {
            "collector_name": request.form.get("collector_name"),
            "agency_name": request.form.get("agency_name"),
            "vehicle_number": request.form.get("vehicle_number"),
            "vehicle_type": request.form.get("vehicle_type"),
            "assigned_zone": request.form.get("assigned_zone"),
            "contact_number": request.form.get("contact_number"),
            "authorization_id": request.form.get("authorization_id"),
            "approved": False  # Civic approval later
        }

        current_user.details = details
        current_user.save()

        return redirect(url_for("collector.dashboard"))

    return render_template("collector/profile_setup.html")

@collector_bp.route("/api/verify_facility/<fid>", methods=["GET", "POST"])
@login_required
def verify_facility(fid):
    try:
        user = User.objects(id=ObjectId(fid), role="facility").first()

        if not user:
            return jsonify({
                "success": False,
                "message": "Facility not found"
            }), 404

        if not user.details:
            return jsonify({
                "success": False,
                "message": "Facility profile incomplete"
            }), 400

        return jsonify({
            "success": True,
            "message": "Facility verified",
            "facility": {
                "name": user.details.get("facility_name"),
                "type": user.details.get("facility_type")
            }
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid Facility ID"
        }), 400
    
