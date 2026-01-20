from .roles import Roles

PERMISSIONS = {
    Roles.CIVIC: [
        "view_all_data",
        "approve_facility",
        "view_heatmap",
        "generate_reports"
    ],

    Roles.FACILITY: [
        "log_waste",
        "generate_qr",
        "request_pickup",
        "view_own_reports"
    ],

    Roles.COLLECTOR: [
        "scan_qr",
        "update_pickup_status"
    ],

    Roles.DISPOSAL: [
        "scan_qr",
        "mark_disposed",
        "upload_certificate"
    ]
}
