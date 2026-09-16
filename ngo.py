from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    get_jwt_identity
)

from extensions import db

from models import (
    User,
    NGOProfile,
    Donation,
    Claim,
    FoodRequest,
    Notification
)

from routes.utils.decorators import role_required
from routes.utils.matching import calculate_match_score


ngo_bp = Blueprint(
    "ngo",
    __name__
)


@ngo_bp.route(
    "/profile",
    methods=["POST"]
)
@role_required("ngo")
def create_profile():

    user_id = int(
        get_jwt_identity()
    )

    existing = NGOProfile.query.filter_by(
        user_id=user_id
    ).first()

    if existing:

        return jsonify({
            "success": False,
            "error":
                "NGO profile already exists"
        }), 409

    data = request.get_json()

    profile = NGOProfile(
        user_id=user_id,
        organization_name=data.get(
            "organization_name"
        ),
        registration_number=data.get(
            "registration_number"
        ),
        address=data.get(
            "address"
        ),
        city=data.get(
            "city"
        ),
        pincode=data.get(
            "pincode"
        ),
        latitude=data.get(
            "latitude"
        ),
        longitude=data.get(
            "longitude"
        ),
        food_types_required=data.get(
            "food_types_required"
        ),
        capacity=data.get(
            "capacity",
            0
        ),
        description=data.get(
            "description"
        )
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({
        "success": True,
        "data":
            profile.to_dict()
    }), 201


@ngo_bp.route(
    "/profile",
    methods=["GET"]
)
@role_required("ngo")
def get_profile():

    user_id = int(
        get_jwt_identity()
    )

    profile = NGOProfile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:

        return jsonify({
            "success": False,
            "error":
                "NGO profile not found"
        }), 404

    return jsonify({
        "success": True,
        "data":
            profile.to_dict()
    })


@ngo_bp.route(
    "/available-donations",
    methods=["GET"]
)
@role_required("ngo")
def available_donations():

    donations = Donation.query.filter_by(
        status="AVAILABLE"
    ).all()

    result = []

    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

    for donation in donations:

        expiry_time = donation.expiry_time
        if expiry_time.tzinfo is None:
            expiry_time = expiry_time.replace(tzinfo=timezone.utc)

        if expiry_time <= datetime.now(timezone.utc):

            donation.status = "EXPIRED"
            donation.priority = "Low"
            donation.freshness_score = 0
            donation.freshness_reason = "Donation expired."
            donation.priority_confidence = 0.0

            continue

        freshness = donation.freshness_summary()
        current_priority = (donation.priority or "").strip()
        if not current_priority or current_priority.lower() not in {"low", "medium", "high", "critical"}:
            donation.priority = freshness["priority"]
        donation.priority = (donation.priority or "Low").strip().title()
        donation.freshness_score = freshness["freshness_score"]
        donation.freshness_reason = freshness["reason"]
        if not donation.priority_confidence:
            donation.priority_confidence = 0.5

        result.append(
            donation.to_dict()
        )

    result.sort(key=lambda item: priority_order.get((item.get("priority") or "Low").title(), 99))
    db.session.commit()

    return jsonify({
        "success": True,
        "count": len(result),
        "data": result
    })


@ngo_bp.route(
    "/claim/<int:donation_id>",
    methods=["POST"]
)
@role_required("ngo")
def claim_donation(donation_id):

    ngo_id = int(
        get_jwt_identity()
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

    if donation.status not in ["AVAILABLE", "MATCHED"]:

        return jsonify({
            "success": False,
            "error":
                "Donation is not available"
        }), 400

    expiry_time = donation.expiry_time
    if expiry_time.tzinfo is None:
        expiry_time = expiry_time.replace(tzinfo=timezone.utc)

    if expiry_time <= datetime.now(timezone.utc):

        donation.status = "EXPIRED"

        db.session.commit()

        return jsonify({
            "success": False,
            "error":
                "Donation has expired"
        }), 400

    existing = Claim.query.filter_by(
        donation_id=donation_id,
        ngo_id=ngo_id
    ).first()

    if existing:

        return jsonify({
            "success": False,
            "error":
                "Donation already claimed"
        }), 409

    claim = Claim(
        donation_id=donation_id,
        ngo_id=ngo_id,
        status="ACCEPTED"
    )

    donation.status = "ACCEPTED"
    donation.claimed_by = ngo_id

    db.session.add(claim)

    donor_notification = Notification(
        user_id=donation.donor_id,
        message=(
            f"Your donation '{donation.food_name}' has been accepted by an NGO."
        ),
        type="DONATION_ACCEPTED"
    )

    db.session.add(
        donor_notification
    )

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Donation claimed successfully"
    })


@ngo_bp.route(
    "/claims",
    methods=["GET"]
)
@role_required("ngo")
def claims():

    ngo_id = int(
        get_jwt_identity()
    )

    claims = Claim.query.filter_by(
        ngo_id=ngo_id
    ).all()

    result = []

    for claim in claims:

        donation = Donation.query.get(
            claim.donation_id
        )

        result.append({
            "claim_id": claim.id,
            "status": claim.status,
            "claimed_at":
                claim.claimed_at.isoformat(),
            "donation":
                donation.to_dict()
                if donation else None
        })

    return jsonify({
        "success": True,
        "data": result
    })


@ngo_bp.route(
    "/food-request",
    methods=["POST"]
)
@role_required("ngo")
def create_food_request():

    ngo_id = int(
        get_jwt_identity()
    )

    data = request.get_json() or {}

    if not data.get("food_type"):
        return jsonify({
            "success": False,
            "error": "food_type is required"
        }), 400

    try:
        quantity_required = float(data.get("quantity_required", 0))
        if quantity_required <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "error": "quantity_required must be a positive number"
        }), 400

    request_data = FoodRequest(
        ngo_id=ngo_id,
        food_type=data.get("food_type"),
        quantity_required=quantity_required,
        servings_required=data.get("servings_required"),
        urgency=(data.get("urgency") or "NORMAL").upper()
    )

    db.session.add(request_data)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": request_data.to_dict()
    }), 201


@ngo_bp.route(
    "/food-requests",
    methods=["GET"]
)
@role_required("ngo")
def food_requests():

    ngo_id = int(
        get_jwt_identity()
    )

    requests = FoodRequest.query.filter_by(
        ngo_id=ngo_id
    ).all()

    return jsonify({
        "success": True,
        "data": [
            item.to_dict()
            for item in requests
        ]
    })
