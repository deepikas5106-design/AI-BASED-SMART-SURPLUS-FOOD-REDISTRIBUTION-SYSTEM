from flask import Blueprint, jsonify

from flask_jwt_extended import (
    get_jwt_identity
)

from extensions import db

from models import (
    Donation,
    Claim,
    Delivery,
    User
)

from routes.utils.decorators import role_required


analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route(
    "/donor",
    methods=["GET"]
)
@role_required("donor")
def donor_analytics():

    user_id = int(
        get_jwt_identity()
    )

    donations = Donation.query.filter_by(
        donor_id=user_id
    ).all()

    return jsonify({
        "success": True,
        "data": {
            "total_donations":
                len(donations),

            "available":
                sum(
                    d.status == "AVAILABLE"
                    for d in donations
                ),

            "accepted":
                sum(
                    d.status == "ACCEPTED"
                    for d in donations
                ),

            "delivered":
                sum(
                    d.status in ["DELIVERED", "COMPLETED"]
                    for d in donations
                ),

            "expired":
                sum(
                    d.status == "EXPIRED"
                    for d in donations
                ),

            "total_food":
                sum(
                    d.quantity
                    for d in donations
                ),

            "total_servings":
                sum(
                    d.servings or 0
                    for d in donations
                )
        }
    })


@analytics_bp.route(
    "/ngo",
    methods=["GET"]
)
@role_required("ngo")
def ngo_analytics():

    user_id = int(
        get_jwt_identity()
    )

    claims = Claim.query.filter_by(
        ngo_id=user_id
    ).all()

    return jsonify({
        "success": True,
        "data": {
            "total_claims":
                len(claims),

            "accepted":
                sum(
                    c.status == "ACCEPTED"
                    for c in claims
                ),

            "completed":
                sum(
                    c.status == "COMPLETED"
                    for c in claims
                ),
            "reward_points":
                sum((u.reward_points or 0) for u in User.query.filter_by(role="donor").all())
        }
    })


@analytics_bp.route(
    "/admin",
    methods=["GET"]
)
@role_required("admin")
def admin_analytics():

    return jsonify({
        "success": True,
        "data": {
            "total_users":
                User.query.count(),

            "total_donations":
                Donation.query.count(),

            "available":
                Donation.query.filter_by(
                    status="AVAILABLE"
                ).count(),

            "accepted":
                Donation.query.filter_by(
                    status="ACCEPTED"
                ).count(),

            "delivered":
                Donation.query.filter(
                    Donation.status.in_(["DELIVERED", "COMPLETED"])
                ).count(),

            "expired":
                Donation.query.filter_by(
                    status="EXPIRED"
                ).count(),

            "total_deliveries":
                Delivery.query.count()
        }
    })
