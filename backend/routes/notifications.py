from flask import Blueprint, jsonify

from flask_jwt_extended import (
    get_jwt_identity
)

from extensions import db

from models import Notification

from routes.utils.decorators import role_required


def create_notification(user_id, message, notification_type="INFO"):
    if user_id is None:
        return None

    notification = Notification(
        user_id=user_id,
        message=message,
        type=notification_type,
        is_read=False,
    )
    db.session.add(notification)
    db.session.commit()
    return notification


notifications_bp = Blueprint(
    "notifications",
    __name__
)


@notifications_bp.route(
    "",
    methods=["GET"]
)
@role_required(
    "donor",
    "ngo",
    "volunteer",
    "admin"
)
def get_notifications():

    user_id = int(
        get_jwt_identity()
    )

    notifications = Notification.query.filter_by(
        user_id=user_id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "data": [
            notification.to_dict()
            for notification in notifications
        ]
    })


@notifications_bp.route(
    "/<int:notification_id>/read",
    methods=["PUT"]
)
@role_required(
    "donor",
    "ngo",
    "volunteer",
    "admin"
)
def mark_read(notification_id):

    user_id = int(
        get_jwt_identity()
    )

    notification = Notification.query.get(
        notification_id
    )

    if not notification:

        return jsonify({
            "success": False,
            "error":
                "Notification not found"
        }), 404

    if notification.user_id != user_id:

        return jsonify({
            "success": False,
            "error":
                "Not authorized"
        }), 403

    notification.is_read = True

    db.session.commit()

    return jsonify({
        "success": True,
        "message":
            "Notification marked as read"
    })
