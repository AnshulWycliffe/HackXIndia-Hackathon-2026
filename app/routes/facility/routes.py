from flask import render_template,request,redirect,url_for,jsonify
from flask_login import login_required,current_user

from . import facility_bp
from app.decorators import role_required
from app.config.roles import Roles
from datetime import datetime
import uuid

from app.models.waste import Waste

@facility_bp.route("/dashboard")
@login_required
@role_required(Roles.FACILITY)
def dashboard():
    recent_waste = (
        Waste.objects(facility_id=current_user)
        .order_by("-created_at")
        .limit(5)
    )
    return render_template("facility/dashboard.html",recent_waste=recent_waste)


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


@facility_bp.route("/api/generate_waste", methods=["POST"])
@login_required
def generate_waste():

    if current_user.role != "facility":
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 403

    data = request.get_json()

    # Basic validation
    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid payload"
        }), 400

    try:
        waste = Waste(
            category=data.get("category"),
            quantity=float(data.get("quantity")),
            storage_location=data.get("storage_location"),
            facility_id=current_user,
            status="pending"
        )
        waste.save()

        return jsonify({
            "success": True,
            "waste_id": str(waste.id),   # 🔥 REAL DB ID
            "category": waste.category,
            "quantity": waste.quantity,
            "facility": current_user.details.get("facility_name"),
            "created_at": waste.created_at.isoformat()
        }), 201

    except Exception as e:
        print(e)
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    

