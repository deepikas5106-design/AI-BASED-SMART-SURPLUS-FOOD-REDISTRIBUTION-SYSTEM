from flask import Blueprint, jsonify

from flask_jwt_extended import get_jwt_identity

from extensions import db

from models import (
    User,
    NGOProfile,
    Donation,
    Delivery
)

from routes.utils.decorators import role_required


admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route(
    "/users",
    methods=["GET"]
)
@role_required("admin")
def users():

    all_users = User.query.all()

    return jsonify({
        "success": True,
        "data": [
            user.to_dict()
            for user in all_users
        ]
    })


@admin_bp.route(
    "/ngos",
    methods=["GET"]
)
@role_required("admin")
def ngos():

    profiles = NGOProfile.query.all()

    return jsonify({
        "success": True,
        "data": [
            profile.to_dict()
            for profile in profiles
        ]
    })


@admin_bp.route(
    "/ngo/<int:ngo_id>/verify",
    methods=["PUT"]
)
@role_required("admin")
def verify_ngo(ngo_id):

    profile = NGOProfile.query.get(
        ngo_id
    )

    if not profile:

        return jsonify({
            "success": False,
            "error":
                "NGO not found"
        }), 404

    profile.verified = True

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "NGO verified"
    })


@admin_bp.route(
    "/donations",
    methods=["GET"]
)
@role_required("admin")
def donations():

    all_donations = Donation.query.all()

    return jsonify({
        "success": True,
        "data": [
            donation.to_dict()
            for donation in all_donations
        ]
    })


@admin_bp.route(
    "/deliveries",
    methods=["GET"]
)
@role_required("admin")
def deliveries():

    all_deliveries = Delivery.query.all()

    return jsonify({
        "success": True,
        "data": [
            delivery.to_dict()
            for delivery in all_deliveries
        ]
    })


@admin_bp.route(
    "/stats",
    methods=["GET"]
)
@role_required("admin")
def stats():

    return jsonify({
        "success": True,
        "data": {
            "users":
                User.query.count(),

            "donations":
                Donation.query.count(),

            "completed_donations":
                Donation.query.filter(
                    Donation.status.in_(["COMPLETED", "DELIVERED"])
                ).count(),

            "pending_donations":
                Donation.query.filter(
                    Donation.status.in_(["AVAILABLE", "MATCHED", "ACCEPTED", "PICKUP_SCHEDULED", "PICKED_UP", "IN_TRANSIT"])
                ).count(),

            "high_priority_food":
                Donation.query.filter(
                    Donation.priority == "HIGH"
                ).count(),

            "ngos":
                NGOProfile.query.count(),

            "deliveries":
                Delivery.query.count(),

            "total_reward_points":
                sum((user.reward_points or 0) for user in User.query.all())
        }
    })
