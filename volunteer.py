from flask import Blueprint, request, jsonify

from flask_jwt_extended import get_jwt_identity

from extensions import db

from models import (
    VolunteerProfile,
    User,
    Delivery
)

from routes.utils.decorators import role_required


volunteer_bp = Blueprint(
    "volunteer",
    __name__
)


@volunteer_bp.route(
    "/profile",
    methods=["POST"]
)
@role_required("volunteer")
def create_profile():

    user_id = int(
        get_jwt_identity()
    )

    if VolunteerProfile.query.filter_by(
        user_id=user_id
    ).first():

        return jsonify({
            "success": False,
            "error":
                "Profile already exists"
        }), 409

    data = request.get_json()

    profile = VolunteerProfile(
        user_id=user_id,
        vehicle_type=data.get(
            "vehicle_type"
        ),
        phone=data.get(
            "phone"
        ),
        city=data.get(
            "city"
        ),
        latitude=data.get(
            "latitude"
        ),
        longitude=data.get(
            "longitude"
        ),
        availability="AVAILABLE"
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "success": True,
        "data":
            profile.to_dict()
    }), 201


@volunteer_bp.route(
    "/profile",
    methods=["GET"]
)
@role_required("volunteer")
def get_profile():

    user_id = int(
        get_jwt_identity()
    )

    profile = VolunteerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:

        return jsonify({
            "success": False,
            "error":
                "Profile not found"
        }), 404

    return jsonify({
        "success": True,
        "data":
            profile.to_dict()
    })


@volunteer_bp.route(
    "/available-deliveries",
    methods=["GET"]
)
@role_required("volunteer")
def available_deliveries():

    deliveries = Delivery.query.filter_by(
        status="PENDING"
    ).all()

    return jsonify({
        "success": True,
        "data": [
            delivery.to_dict()
            for delivery in deliveries
        ]
    })


@volunteer_bp.route(
    "/my-deliveries",
    methods=["GET"]
)
@role_required("volunteer")
def my_deliveries():

    user_id = int(
        get_jwt_identity()
    )

    deliveries = Delivery.query.filter_by(
        volunteer_id=user_id
    ).all()

    return jsonify({
        "success": True,
        "data": [
            delivery.to_dict()
            for delivery in deliveries
        ]
    })


@volunteer_bp.route(
    "/delivery/<int:delivery_id>/accept",
    methods=["POST"]
)
@role_required("volunteer")
def accept_delivery(delivery_id):

    user_id = int(
        get_jwt_identity()
    )

    delivery = Delivery.query.get(
        delivery_id
    )

    if not delivery:

        return jsonify({
            "success": False,
            "error":
                "Delivery not found"
        }), 404

    if delivery.status != "PENDING":

        return jsonify({
            "success": False,
            "error":
                "Delivery unavailable"
        }), 400

    delivery.volunteer_id = user_id
    delivery.status = "ASSIGNED"

    profile = VolunteerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if profile:

        profile.availability = "BUSY"

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Delivery accepted",
        "data":
            delivery.to_dict()
    })


@volunteer_bp.route(
    "/delivery/<int:delivery_id>/pickup",
    methods=["POST"]
)
@role_required("volunteer")
def pickup(delivery_id):

    user_id = int(
        get_jwt_identity()
    )

    delivery = Delivery.query.get(
        delivery_id
    )

    if not delivery:

        return jsonify({
            "success": False,
            "error":
                "Delivery not found"
        }), 404

    if delivery.volunteer_id != user_id:

        return jsonify({
            "success": False,
            "error":
                "Not authorized"
        }), 403

    delivery.status = "PICKED_UP"

    if delivery.donation_id:
        donation = Donation.query.get(delivery.donation_id)
        if donation:
            donation.status = "PICKED_UP"

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Food picked up"
    })


@volunteer_bp.route(
    "/delivery/<int:delivery_id>/start",
    methods=["POST"]
)
@role_required("volunteer")
def start_delivery(delivery_id):

    user_id = int(
        get_jwt_identity()
    )

    delivery = Delivery.query.get(
        delivery_id
    )

    if not delivery:

        return jsonify({
            "success": False,
            "error":
                "Delivery not found"
        }), 404

    if delivery.volunteer_id != user_id:

        return jsonify({
            "success": False,
            "error":
                "Not authorized"
        }), 403

    delivery.status = "IN_TRANSIT"

    if delivery.donation_id:
        donation = Donation.query.get(delivery.donation_id)
        if donation:
            donation.status = "IN_TRANSIT"

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Delivery started"
    })


@volunteer_bp.route(
    "/delivery/<int:delivery_id>/complete",
    methods=["POST"]
)
@role_required("volunteer")
def complete_delivery(delivery_id):

    user_id = int(
        get_jwt_identity()
    )

    delivery = Delivery.query.get(
        delivery_id
    )

    if not delivery:

        return jsonify({
            "success": False,
            "error":
                "Delivery not found"
        }), 404

    if delivery.volunteer_id != user_id:

        return jsonify({
            "success": False,
            "error":
                "Not authorized"
        }), 403

    delivery.status = "DELIVERED"

    delivery.actual_delivery_time = (
        datetime.now(timezone.utc)
    )

    from models import Donation

    donation = Donation.query.get(
        delivery.donation_id
    )

    if donation:

        donation.status = "COMPLETED"
        donation.completed_at = datetime.now(timezone.utc)
        if donation.reward_points is None or donation.reward_points <= 0:
            donation.reward_points = 50

        donor = User.query.get(donation.donor_id)
        if donor:
            donor.reward_points = (donor.reward_points or 0) + donation.reward_points

    profile = VolunteerProfile.query.filter_by(
        user_id=user_id
    ).first()

    if profile:

        profile.availability = "AVAILABLE"

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Delivery completed"
    })
