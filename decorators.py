from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User


def role_required(*required_roles):
    """
    Restrict an API route to one or more user roles.

    Example:

        @role_required("admin")

    or:

        @role_required("ngo", "volunteer", "admin")
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Verify JWT token exists and is valid
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({
                    "success": False,
                    "message": "Login required"
                }), 401

            # Get user ID from JWT
            user_id = get_jwt_identity()

            # Get user from database
            user = User.query.get(user_id)

            if not user:
                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404

            # Get the user's role
            user_role = user.role

            # Make sure a role exists
            if not user_role:
                return jsonify({
                    "success": False,
                    "message": "User role not found"
                }), 403

            # Convert role to lowercase for reliable comparison
            user_role = str(user_role).lower()

            # Convert all allowed roles to lowercase
            allowed_roles = [
                str(role).lower()
                for role in required_roles
            ]

            # Check whether the user's role is allowed
            if user_role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Access denied"
                }), 403

            # User is authorized
            return func(*args, **kwargs)

        return wrapper

    return decorator