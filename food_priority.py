from datetime import datetime

from flask import Blueprint, jsonify, request

from ml.predict import predict_food_priority

food_priority_bp = Blueprint("food_priority", __name__)


@food_priority_bp.route("/predict", methods=["POST"])
def predict_food_priority_route():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "expiry_hours",
        "quantity",
        "food_type",
        "donation_age_hours",
    ]

    missing = [field for field in required_fields if field not in data or data[field] in (None, "")]

    if missing:
        return jsonify({
            "success": False,
            "error": f"Missing required fields: {', '.join(missing)}"
        }), 400

    prediction = predict_food_priority(
        expiry_hours=data.get("expiry_hours"),
        quantity=data.get("quantity"),
        food_type=data.get("food_type"),
        donation_age_hours=data.get("donation_age_hours"),
        storage_condition=data.get("storage_condition"),
        food_category=data.get("food_category"),
    )

    if not prediction["success"]:
        return jsonify(prediction), 400

    return jsonify({
        "success": True,
        "priority": prediction["priority"],
        "confidence": prediction["confidence"],
        "probabilities": prediction.get("probabilities", {}),
    })
