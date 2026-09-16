from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from extensions import db
from models import Donation
from ml.predict import predict_food_priority
from routes.notifications import create_notification
from routes.utils.freshness import calculate_freshness_priority


donations_bp = Blueprint(
    "donations",
    __name__
)


@donations_bp.route(
    "",
    methods=["POST"]
)
@jwt_required()
def create_donation():

    user_id = int(
        get_jwt_identity()
    )

    data = request.get_json()

    required = [
        "food_name",
        "quantity",
        "pickup_location",
        "expiry_time"
    ]

    for field in required:

        if not data.get(field):

            return jsonify({
                "success": False,
                "error":
                    f"{field} is required"
            }), 400

    try:

        quantity = float(
            data["quantity"]
        )

        if quantity <= 0:
            raise ValueError

    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "error":
                "Quantity must be positive"
        }), 400

    try:

        expiry = datetime.fromisoformat(
            data["expiry_time"]
        )
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)

    except ValueError:

        return jsonify({
            "success": False,
            "error":
                "Invalid expiry_time format"
        }), 400

    if expiry <= datetime.now(timezone.utc):

        return jsonify({
            "success": False,
            "error":
                "Expiry time must be in the future"
        }), 400

    food_type = data.get("food_type") or "packaged"
    storage_condition = data.get("storage_condition") or "room_temperature"
    food_category = data.get("food_category") or "unknown"

    donation_age_hours = float(data.get("donation_age_hours") or 0)
    expiry_hours = max(0.01, round((expiry - datetime.now(timezone.utc)).total_seconds() / 3600, 2))

    prediction = predict_food_priority(
        expiry_hours=expiry_hours,
        quantity=quantity,
        food_type=food_type,
        donation_age_hours=donation_age_hours,
        storage_condition=storage_condition,
        food_category=food_category,
    )

    if not prediction["success"]:
        return jsonify(prediction), 400

    donation = Donation(

        donor_id=user_id,

        food_name=data["food_name"],

        food_type=food_type,

        food_category=food_category,

        storage_condition=storage_condition,

        quantity=quantity,

        unit=data.get(
            "unit",
            "kg"
        ),

        servings=data.get(
            "servings"
        ),

        description=data.get(
            "description"
        ),

        image=data.get(
            "image"
        ),

        pickup_location=data[
            "pickup_location"
        ],

        latitude=data.get(
            "latitude"
        ),

        longitude=data.get(
            "longitude"
        ),

        expiry_time=expiry,
        expiry_hours=expiry_hours,
        donation_age_hours=donation_age_hours,
        status="AVAILABLE",
        priority=prediction["priority"],
        priority_confidence=prediction["confidence"],
    )

    freshness = calculate_freshness_priority(
        expiry,
        donation.food_type
    )
    donation.status = "AVAILABLE"
    donation.priority = prediction["priority"]
    donation.priority_confidence = prediction["confidence"]
    donation.freshness_score = freshness["freshness_score"]
    donation.freshness_reason = freshness["reason"]

    db.session.add(donation)
    db.session.commit()

    create_notification(
        user_id=user_id,
        message=(
            f"New donation submitted: {donation.food_name} "
            f"({donation.priority})"
        ),
        notification_type="NEW_DONATION",
    )

    response = donation.to_dict()
    response["freshness"] = freshness
    response["ml_priority"] = {
        "priority": donation.priority,
        "confidence": donation.priority_confidence
    }

    return jsonify({
        "success": True,
        "message":
            "Donation created successfully",
        "data":
            response
    }), 201


@donations_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
def get_donations():

    donations = Donation.query.order_by(
        Donation.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "count": len(donations),
        "data": [
            donation.to_dict()
            for donation in donations
        ]
    })


@donations_bp.route(
    "/my",
    methods=["GET"]
)
@jwt_required()
def my_donations():

    user_id = int(
        get_jwt_identity()
    )

    donations = Donation.query.filter_by(
        donor_id=user_id
    ).order_by(
        Donation.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "data": [
            donation.to_dict()
            for donation in donations
        ]
    })


@donations_bp.route(
    "/<int:donation_id>",
    methods=["GET"]
)
@jwt_required()
def get_donation(donation_id):

    donation = Donation.query.get(
        donation_id
    )

    if not donation:

        return jsonify({
            "success": False,
            "error":
                "Donation not found"
        }), 404

    return jsonify({
        "success": True,
        "data":
            donation.to_dict()
    })


@donations_bp.route(
    "/<int:donation_id>/qr",
    methods=["GET"]
)
@jwt_required()
def donation_qr(donation_id):
    donation = Donation.query.get(donation_id)

    if not donation:
        return jsonify({
            "success": False,
            "error": "Donation not found"
        }), 404

    try:
        import base64
        import io

        import qrcode

        payload = f"foodredistribute://donation/{donation.id}"
        qr_image = qrcode.make(payload)
        buffer = io.BytesIO()
        qr_image.save(buffer, format="PNG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return jsonify({
            "success": True,
            "data": {
                "donation_id": donation.id,
                "qr_code": image_b64,
                "payload": payload,
                "status": donation.status,
                "verified": bool(donation.qr_code)
            }
        })
    except Exception as exc:
        return jsonify({
            "success": False,
            "error": f"QR generation failed: {str(exc)}"
        }), 500


@donations_bp.route(
    "/<int:donation_id>",
    methods=["PUT"]
)
@jwt_required()
def update_donation(donation_id):

    user_id = int(
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

    if donation.donor_id != user_id:

        return jsonify({
            "success": False,
            "error":
                "You can only modify your donations"
        }), 403

    if donation.status != "AVAILABLE":

        return jsonify({
            "success": False,
            "error":
                "Donation cannot be modified now"
        }), 400

    data = request.get_json()

    fields = [
        "food_name",
        "food_type",
        "quantity",
        "unit",
        "servings",
        "description",
        "pickup_location",
        "latitude",
        "longitude"
    ]

    for field in fields:

        if field in data:

            setattr(
                donation,
                field,
                data[field]
            )

    if "expiry_time" in data:

        try:

            donation.expiry_time = (
                datetime.fromisoformat(
                    data["expiry_time"]
                )
            )

        except ValueError:

            return jsonify({
                "success": False,
                "error":
                    "Invalid expiry_time"
            }), 400

    db.session.commit()

    expiry_hours = max(0.01, round((donation.expiry_time - datetime.now(timezone.utc)).total_seconds() / 3600, 2))
    donation.expiry_hours = expiry_hours
    donation.donation_age_hours = donation.donation_age_hours or 0
    prediction = predict_food_priority(
        expiry_hours=donation.expiry_hours,
        quantity=donation.quantity,
        food_type=donation.food_type or "packaged",
        donation_age_hours=donation.donation_age_hours,
        storage_condition=donation.storage_condition or "room_temperature",
        food_category=donation.food_category or "unknown",
    )

    freshness = calculate_freshness_priority(
        donation.expiry_time,
        donation.food_type
    )
    donation.priority = prediction["priority"] if prediction["success"] else freshness["priority"]
    donation.priority_confidence = prediction["confidence"] if prediction["success"] else 0.0
    donation.freshness_score = freshness["freshness_score"]
    donation.freshness_reason = freshness["reason"]

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Donation updated",
        "data":
            donation.to_dict()
    })


@donations_bp.route(
    "/<int:donation_id>/cancel",
    methods=["POST"]
)
@jwt_required()
def cancel_donation(donation_id):

    user_id = int(
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

    if donation.donor_id != user_id:

        return jsonify({
            "success": False,
            "error":
                "Not authorized"
        }), 403

    donation.status = "CANCELLED"

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Donation cancelled"
    })


@donations_bp.route(
    "/<int:donation_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_donation(donation_id):

    user_id = int(
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

    if donation.donor_id != user_id:

        return jsonify({
            "success": False,
            "error":
                "Not authorized"
        }), 403

    donation.status = "CANCELLED"

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Donation cancelled"
    })
