from flask import render_template,jsonify, request,redirect,url_for
from flask_login import login_required, current_user

from bson import ObjectId

from . import disposal_bp
from app.decorators import role_required
from app.config.roles import Roles
from app.models.waste import Waste
from app.models.audit_log import AuditLog

from datetime import datetime
from zoneinfo import ZoneInfo



@disposal_bp.route("/dashboard")
@login_required
def dashboard():

    IST = ZoneInfo("Asia/Kolkata")

    start_of_today = datetime.now(IST).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # 1️⃣ Assigned today (collected but not disposed)
    assigned_today = Waste.objects(
        status="collected",
        created_at__gte=start_of_today
    ).count()

    # 2️⃣ Disposed today (sum of quantity)
    disposed_today_qs = Waste.objects(
        status="disposed",
        disposed_by=current_user,
        created_at__gte=start_of_today
    )

    disposed_today_kg = sum(w.quantity for w in disposed_today_qs)

    # 3️⃣ List of disposed waste (for bottom section)
    disposed_waste = disposed_today_qs.order_by("-created_at")

    return render_template(
        "disposal/dashboard.html",
        assigned_today=assigned_today,
        disposed_today_kg=disposed_today_kg,
        disposed_waste=disposed_waste
    )


@disposal_bp.route("/profile/setup", methods=["GET", "POST"])
@login_required
def profile_setup():
    
    if current_user.role != "disposal":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        details = {
            "unit_name": request.form.get("unit_name"),
            "facility_type": request.form.get("facility_type"),
            "license_no": request.form.get("license_no"),
            "methods": request.form.getlist("methods"),
            "capacity_per_day": request.form.get("capacity_per_day"),
            "operating_area": request.form.get("operating_area"),
            "contact_person": request.form.get("contact_person"),
            "contact_number": request.form.get("contact_number"),
            "approved": False
        }

        current_user.details = details
        current_user.save()

        return redirect(url_for("disposal.dashboard"))

    return render_template("disposal/profile_setup.html")


@disposal_bp.route("/api/verify_waste/<wid>", methods=["GET"])
@login_required
def verify_waste(wid):
    try:
        waste = Waste.objects(id=ObjectId(wid), status="collected").first()

        if not waste:
            return jsonify({
                "success": False,
                "message": "Waste not eligible for disposal"
            }), 404

        return jsonify({
            "success": True,
            "waste": {
                "id": str(waste.id),
                "category": waste.category,
                "quantity": waste.quantity,
                "facility": waste.facility_id.details.get("facility_name"),
                "agency_name": waste.collected_by.details.get("agency_name")
            }
        })

    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid Waste ID"
        }), 400
    

@disposal_bp.route("/api/mark_disposed/<wid>", methods=["POST"])
@login_required
def mark_disposed(wid):

    method = request.json.get("method")

    waste = Waste.objects(id=ObjectId(wid)).first()

    if not waste:
        return jsonify({"success": False}), 404

    waste.update(
        set__status="disposed",
        set__disposed_by=current_user.id,
        set__disposal_method=method
    )

    AuditLog(
        action="WASTE_DISPOSED",
        actor_role="disposal",
        actor_id=current_user,
        target_type="waste",
        target_id=str(waste.id),
        message=f"Disposed using {method}"
    ).save()


    return jsonify({"success": True})
