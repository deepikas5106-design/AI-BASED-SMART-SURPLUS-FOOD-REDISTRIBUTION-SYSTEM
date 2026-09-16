from flask import Flask, jsonify

from flask_cors import CORS
from sqlalchemy import text

from config import Config

from extensions import db, jwt

from routes.auth import auth_bp
from routes.donations import donations_bp
from routes.food_priority import food_priority_bp
from routes.ngo import ngo_bp
from routes.volunteer import volunteer_bp
from routes.delivery import delivery_bp
from routes.notifications import notifications_bp
from routes.analytics import analytics_bp
from routes.admin import admin_bp
from models import User


def ensure_demo_users():
    demo_users = [
        ("Demo Donor", "donor@example.com", "Donor@123", "donor"),
        ("Demo NGO", "ngo@example.com", "Ngo@123", "ngo"),
        ("Demo Volunteer", "volunteer@example.com", "Volunteer@123", "volunteer"),
        ("System Admin", "admin@example.com", "Admin@123", "admin"),
    ]

    existing_emails = {
        email for email in db.session.execute(
            db.select(User.email)
        ).scalars().all()
    }

    for name, email, password, role in demo_users:
        if email in existing_emails:
            continue

        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        existing_emails.add(email)

    db.session.commit()


def ensure_ml_schema():
    inspector = db.inspect(db.engine)
    columns = {column["name"] for column in inspector.get_columns("donations")}

    migration_columns = {
        "food_category": "VARCHAR(50) DEFAULT 'unknown'",
        "storage_condition": "VARCHAR(50) DEFAULT 'room_temperature'",
        "expiry_hours": "FLOAT DEFAULT 0.0",
        "donation_age_hours": "FLOAT DEFAULT 0.0",
        "priority_confidence": "FLOAT DEFAULT 0.0",
    }

    for name, ddl in migration_columns.items():
        if name in columns:
            continue

        db.session.execute(text(f"ALTER TABLE donations ADD COLUMN {name} {ddl}"))

    db.session.commit()


def create_app():

    app = Flask(__name__)

    app.config.from_object(
        Config
    )

    db.init_app(app)

    jwt.init_app(app)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        donations_bp,
        url_prefix="/api/donations"
    )

    app.register_blueprint(
        food_priority_bp,
        url_prefix="/api/food-priority"
    )

    app.register_blueprint(
        ngo_bp,
        url_prefix="/api/ngo"
    )

    app.register_blueprint(
        volunteer_bp,
        url_prefix="/api/volunteer"
    )

    app.register_blueprint(
        delivery_bp,
        url_prefix="/api/delivery"
    )

    app.register_blueprint(
        notifications_bp,
        url_prefix="/api/notifications"
    )

    app.register_blueprint(
        analytics_bp,
        url_prefix="/api/analytics"
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/admin"
    )

    with app.app_context():

        db.create_all()
        ensure_ml_schema()
        ensure_demo_users()

    @app.route("/")
    def home():

        return jsonify({
            "success": True,
            "message":
                "Surplus Food Redistribution API",
            "status": "running"
        })

    @app.route("/api/health")
    def health():

        return jsonify({
            "success": True,
            "status": "healthy"
        })

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )