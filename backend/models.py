from datetime import datetime, timezone

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    reward_points = db.Column(
        db.Integer,
        default=0
    )

    phone = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.String(255)
    )

    city = db.Column(
        db.String(100)
    )

    pincode = db.Column(
        db.String(10)
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "reward_points": self.reward_points or 0,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "pincode": self.pincode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "is_active": self.is_active
        }


class NGOProfile(db.Model):

    __tablename__ = "ngo_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    organization_name = db.Column(
        db.String(150),
        nullable=False
    )

    registration_number = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.String(255)
    )

    city = db.Column(
        db.String(100)
    )

    pincode = db.Column(
        db.String(10)
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    food_types_required = db.Column(
        db.String(255)
    )

    capacity = db.Column(
        db.Integer,
        default=0
    )

    description = db.Column(
        db.Text
    )

    verified = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "organization_name":
                self.organization_name,
            "registration_number":
                self.registration_number,
            "address": self.address,
            "city": self.city,
            "pincode": self.pincode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "food_types_required":
                self.food_types_required,
            "capacity": self.capacity,
            "description":
                self.description,
            "verified": self.verified
        }


class VolunteerProfile(db.Model):

    __tablename__ = "volunteer_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    vehicle_type = db.Column(
        db.String(50)
    )

    phone = db.Column(
        db.String(20)
    )

    city = db.Column(
        db.String(100)
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    availability = db.Column(
        db.String(20),
        default="AVAILABLE"
    )

    verified = db.Column(
        db.Boolean,
        default=False
    )

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_type":
                self.vehicle_type,
            "phone": self.phone,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "availability":
                self.availability,
            "verified":
                self.verified
        }


class Donation(db.Model):

    __tablename__ = "donations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    food_name = db.Column(
        db.String(150),
        nullable=False
    )

    food_type = db.Column(
        db.String(100)
    )

    food_category = db.Column(
        db.String(50),
        default="unknown"
    )

    storage_condition = db.Column(
        db.String(50),
        default="room_temperature"
    )

    quantity = db.Column(
        db.Float,
        nullable=False
    )

    unit = db.Column(
        db.String(20),
        default="kg"
    )

    servings = db.Column(
        db.Integer
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    pickup_location = db.Column(
        db.String(255),
        nullable=False
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    expiry_time = db.Column(
        db.DateTime,
        nullable=False
    )

    expiry_hours = db.Column(
        db.Float,
        default=0.0
    )

    donation_age_hours = db.Column(
        db.Float,
        default=0.0
    )

    status = db.Column(
        db.String(30),
        default="AVAILABLE"
    )

    priority = db.Column(
        db.String(20),
        default="LOW"
    )

    priority_confidence = db.Column(
        db.Float,
        default=0.0
    )

    freshness_score = db.Column(
        db.Integer,
        default=0
    )

    freshness_reason = db.Column(
        db.Text
    )

    reward_points = db.Column(
        db.Integer,
        default=0
    )

    qr_code = db.Column(
        db.String(255)
    )

    claimed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(
        db.DateTime
    )

    def freshness_summary(self):
        from routes.utils.freshness import calculate_freshness_priority

        return calculate_freshness_priority(
            self.expiry_time,
            self.food_type
        )

    def to_dict(self):

        freshness = self.freshness_summary()

        return {
            "id": self.id,
            "donor_id": self.donor_id,
            "food_name": self.food_name,
            "food_type": self.food_type,
            "food_category": self.food_category,
            "storage_condition": self.storage_condition,
            "quantity": self.quantity,
            "unit": self.unit,
            "servings": self.servings,
            "description": self.description,
            "image": self.image,
            "pickup_location":
                self.pickup_location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "expiry_time":
                self.expiry_time.isoformat(),
            "expiry_hours":
                self.expiry_hours or freshness["hours_left"],
            "donation_age_hours":
                self.donation_age_hours or 0,
            "status": self.status,
            "claimed_by":
                self.claimed_by,
            "priority":
                self.priority or freshness["priority"],
            "priority_confidence":
                self.priority_confidence or 0.0,
            "freshness_score":
                self.freshness_score or freshness["freshness_score"],
            "freshness_reason":
                self.freshness_reason or freshness["reason"],
            "hours_left":
                freshness["hours_left"],
            "reward_points":
                self.reward_points or 0,
            "qr_code": self.qr_code,
            "created_at":
                self.created_at.isoformat(),
            "completed_at":
                self.completed_at.isoformat()
                if self.completed_at else None
        }


class FoodRequest(db.Model):

    __tablename__ = "food_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    ngo_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    food_type = db.Column(
        db.String(100),
        nullable=False
    )

    quantity_required = db.Column(
        db.Float,
        nullable=False
    )

    servings_required = db.Column(
        db.Integer
    )

    urgency = db.Column(
        db.String(20),
        default="NORMAL"
    )

    status = db.Column(
        db.String(20),
        default="OPEN"
    )

    requested_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):

        return {
            "id": self.id,
            "ngo_id": self.ngo_id,
            "food_type": self.food_type,
            "quantity_required":
                self.quantity_required,
            "servings_required":
                self.servings_required,
            "urgency": self.urgency,
            "status": self.status,
            "requested_at":
                self.requested_at.isoformat()
        }


class Claim(db.Model):

    __tablename__ = "claims"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey("donations.id"),
        nullable=False
    )

    ngo_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="ACCEPTED"
    )

    claimed_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class Delivery(db.Model):

    __tablename__ = "deliveries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey("donations.id"),
        nullable=False
    )

    ngo_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    volunteer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    pickup_location = db.Column(
        db.String(255)
    )

    delivery_location = db.Column(
        db.String(255)
    )

    pickup_time = db.Column(
        db.DateTime
    )

    estimated_delivery_time = db.Column(
        db.DateTime
    )

    actual_delivery_time = db.Column(
        db.DateTime
    )

    status = db.Column(
        db.String(30),
        default="PENDING"
    )

    def to_dict(self):

        return {
            "id": self.id,
            "donation_id":
                self.donation_id,
            "ngo_id": self.ngo_id,
            "volunteer_id":
                self.volunteer_id,
            "pickup_location":
                self.pickup_location,
            "delivery_location":
                self.delivery_location,
            "pickup_time":
                self.pickup_time.isoformat()
                if self.pickup_time else None,
            "estimated_delivery_time":
                self.estimated_delivery_time.isoformat()
                if self.estimated_delivery_time else None,
            "actual_delivery_time":
                self.actual_delivery_time.isoformat()
                if self.actual_delivery_time else None,
            "status": self.status
        }


class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.String(500),
        nullable=False
    )

    type = db.Column(
        db.String(50)
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):

        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "type": self.type,
            "is_read": self.is_read,
            "created_at":
                self.created_at.isoformat()
        }


class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey("donations.id"),
        nullable=False
    )

    reviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reviewed_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )