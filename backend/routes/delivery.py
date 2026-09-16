from flask import Blueprint, request, jsonify

from flask_jwt_extended import get_jwt_identity

from extensions import db

from models import (
    Delivery,
    Donation,
    Claim
)

from routes.utils.decorators import role_required


delivery_bp = Blueprint(
    "delivery",
    __name__
)


@delivery_bp.route(
    "",
    methods=["POST"]
)
@role_required("ngo")
def create_delivery():

    ngo_id = int(
        get_jwt_identity()
    )

    data = request.get_json()

    donation_id = data.get(
        "donation_id"
    )

    donation = Donation.query.get(
        donation_id
    )

    if not donation:

        return jsonify({
            "success": False,
            "error":
                "Donation not found"
        }), 404

    claim = Claim.query.filter_by(
        donation_id=donation_id,
        ngo_id=ngo_id,
        status="ACCEPTED"
    ).first()

    if not claim:

        return jsonify({
            "success": False,
            "error":
                "NGO has not claimed this donation"
        }), 403

    delivery = Delivery(
        donation_id=donation_id,
        ngo_id=ngo_id,
        pickup_location=
            donation.pickup_location,
        delivery_location=
            data.get(
                "delivery_location"
            ),
        status="PENDING"
    )

    db.session.add(delivery)

    donation.status = "PICKUP_SCHEDULED"

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Delivery created",
        "data":
            delivery.to_dict()
    }), 201


@delivery_bp.route(
    "/<int:delivery_id>",
    methods=["GET"]
)
@role_required(
    "ngo",
    "volunteer",
    "admin"
)
def get_delivery(delivery_id):

    delivery = Delivery.query.get(
        delivery_id
    )

    if not delivery:

        return jsonify({
            "success": False,
            "error":
                "Delivery not found"
        }), 404

    return jsonify({
        "success": True,
        "data":
            delivery.to_dict()
    })
