from flask import render_template, url_for,redirect,request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId

from . import collector_bp
from app.decorators import role_required
from app.config.roles import Roles
from app.config.constants import ACCOUNT_STATUS
from app.models.waste import Waste
from app.models.audit_log import AuditLog
from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.user import User


@collector_bp.route("/dashboard")
@login_required
@role_required(Roles.COLLECTOR)
def dashboard():
    recent_waste = (
        Waste.objects()
        .order_by("-created_at")
        .limit(5)
    )

    IST = ZoneInfo("Asia/Kolkata")

    start_of_today = datetime.now(IST).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    today_waste_qs = Waste.objects(
        created_at__gte=start_of_today
    )

    pending_pickup = today_waste_qs.filter(
        status="pending"
    ).count()

    total_collected = today_waste_qs.filter(
        status="collected"
    ).count()
    return render_template("collector/dashboard.html",
                           recent_waste=recent_waste,
                           pending_pickup=pending_pickup,
                           total_collected=total_collected)


@collector_bp.route("/profile/setup", methods=["GET", "POST"])
@login_required
def profile_setup():

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


@collector_bp.route("/api/collect_waste/<bid>", methods=["GET", "POST"])
@login_required
def collect_waste(bid):
    try:
        waste = Waste.objects(id=ObjectId(bid)).first()

        if not waste:
            return jsonify({
                "success": False,
                "message": "Waste not found"
            }), 404

        if not waste.facility_id:
            return jsonify({
                "success": False,
                "message": "Facility profile incomplete"
            }), 400
        waste.status = "collected"
        waste.collected_by = current_user.id
        waste.save()

        AuditLog(
            action="WASTE_COLLECTED",
            actor_role="collector",
            actor_id=current_user,
            target_type="waste",
            target_id=str(waste.id),
            message="Waste batch collected via QR scan"
        ).save()


        return jsonify({
            "success": True,
            "message": "Waste Collected"
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid Waste ID"
        }), 400


@collector_bp.route("/api/report_issue", methods=["POST"])
@login_required
def report_issue():

    data = request.get_json()

    waste_id = data.get("waste_id")
    issue_type = data.get("issue_type")
    remarks = data.get("remarks")

    if not waste_id or not issue_type:
        return jsonify({
            "success": False,
            "message": "Invalid issue data"
        }), 400

    waste = Waste.objects(id=ObjectId(waste_id)).first()

    if not waste:
        return jsonify({
            "success": False,
            "message": "Waste not found"
        }), 404

    waste.update(
        set__status="pending",  # stays pending
        set__collected_by=current_user.id,
        set__issue_type= issue_type,
        set__remarks= remarks
        
    )

    return jsonify({
        "success": True,
        "message": "Issue reported successfully"
    }), 200

