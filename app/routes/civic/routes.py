from flask import Blueprint, render_template,redirect
from flask_login import login_required, current_user
from datetime import datetime
from zoneinfo import ZoneInfo

from app.models.user import User
from app.models.waste import Waste
from app.models.audit_log import AuditLog

from app.config.roles import Roles
from app.config.constants import ACCOUNT_STATUS

from . import civic_bp

IST = ZoneInfo("Asia/Kolkata")


@civic_bp.route("/dashboard")
@login_required
def dashboard():

    # Role guard
    if current_user.role != Roles.CIVIC:
        return redirect("/auth/login")

    start_of_today = datetime.now(IST).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # --- KPIs ---
    total_facilities = User.objects(role=Roles.FACILITY).count()
    total_collectors = User.objects(role=Roles.COLLECTOR).count()

    waste_today_kg = sum(
        w.quantity for w in Waste.objects(
            created_at__gte=start_of_today
        )
    )

    disposed_today_kg = sum(
        w.quantity for w in Waste.objects(
            status="disposed",
            created_at__gte=start_of_today
        )
    )

    # --- Pending Approvals ---
    pending_users = User.objects(
        role__in=[Roles.FACILITY, Roles.COLLECTOR, Roles.DISPOSAL],
        status=ACCOUNT_STATUS[0]
    )

    # --- Live Stats ---
    total_generated = Waste.objects(status="pending").count()
    total_collected = Waste.objects(status="collected").count()
    total_disposed = Waste.objects(status="disposed").count()


    audit_logs = AuditLog.objects().order_by("-created_at")[:50]



    return render_template(
        "civic/dashboard.html",
        total_facilities=total_facilities,
        total_collectors=total_collectors,
        waste_today_kg=waste_today_kg,
        disposed_today_kg=disposed_today_kg,
        pending_users=pending_users,
        total_generated=total_generated,
        total_collected=total_collected,
        total_disposed=total_disposed,
        audit_logs=audit_logs
    )


from flask import jsonify
from bson import ObjectId


@civic_bp.route("/api/approve_user/<uid>", methods=["POST"])
@login_required
def approve_user(uid):

    if current_user.role != Roles.CIVIC:
        return jsonify({"success": False}), 403

    user = User.objects(id=ObjectId(uid)).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user["status"] = ACCOUNT_STATUS[1]
    user.save()

    return jsonify({
        "success": True,
        "message": "User approved"
    })


@civic_bp.route("/api/reject_user/<uid>", methods=["POST"])
@login_required
def reject_user(uid):

    if current_user.role != Roles.CIVIC:
        return jsonify({"success": False}), 403

    user = User.objects(id=ObjectId(uid)).first()

    if not user:
        return jsonify({"success": False}), 404

    # Optional: mark rejected flag
    user["status"] = ACCOUNT_STATUS[2]
    user.save()

    return jsonify({
        "success": True,
        "message": "User rejected"
    })
