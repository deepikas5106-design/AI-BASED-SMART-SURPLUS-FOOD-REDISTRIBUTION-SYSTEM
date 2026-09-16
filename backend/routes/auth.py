from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from extensions import db
from models import User


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "error": "JSON body required"
        }), 400

    required = [
        "name",
        "email",
        "password",
        "role"
    ]

    for field in required:

        if not data.get(field):

            return jsonify({
                "success": False,
                "error":
                    f"{field} is required"
            }), 400

    email = data["email"].strip().lower()

    if User.query.filter_by(
        email=email
    ).first():

        return jsonify({
            "success": False,
            "error":
                "Email already registered"
        }), 409

    role = data["role"].lower()

    if role == "individual":
        role = "donor"

    allowed_roles = [
        "donor",
        "ngo",
        "volunteer",
        "admin"
    ]

    if role not in allowed_roles:

        return jsonify({
            "success": False,
            "error": "Invalid role"
        }), 400

    user = User(
        name=data["name"],
        email=email,
        role=role,
        phone=data.get("phone"),
        address=data.get("address"),
        city=data.get("city"),
        pincode=data.get("pincode"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    user.set_password(
        data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Registration successful",
        "data":
            user.to_dict()
    }), 201


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "error": "JSON body required"
        }), 400

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    user = User.query.filter_by(
        email=email
    ).first()

    if (
        not user
        or not user.check_password(password)
    ):

        return jsonify({
            "success": False,
            "error":
                "Invalid email or password"
        }), 401

    if not user.is_active:

        return jsonify({
            "success": False,
            "error":
                "Account is inactive"
        }), 403

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "success": True,
        "message":
            "Login successful",
        "access_token": token,
        "user":
            user.to_dict()
    })


@auth_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def me():

    user_id = int(
        get_jwt_identity()
    )

    user = User.query.get(
        user_id
    )

    if not user:

        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "data":
            user.to_dict()
    })


@auth_bp.route(
    "/logout",
    methods=["POST"]
)
@jwt_required()
def logout():

    return jsonify({
        "success": True,
        "message":
            "Logout successful"
    })
