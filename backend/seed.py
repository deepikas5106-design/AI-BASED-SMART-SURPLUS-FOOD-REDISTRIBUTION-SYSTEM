from app import app
from extensions import db
from models import User


def create_user(
    name,
    email,
    password,
    role
):

    existing = User.query.filter_by(
        email=email
    ).first()

    if existing:

        print(
            f"{email} already exists"
        )

        return

    user = User(
        name=name,
        email=email,
        role=role
    )

    user.set_password(
        password
    )

    db.session.add(user)

    print(
        f"Created {role}: {email}"
    )


with app.app_context():

    db.create_all()

    create_user(
        "Demo Donor",
        "donor@example.com",
        "Donor@123",
        "donor"
    )

    create_user(
        "Demo NGO",
        "ngo@example.com",
        "Ngo@123",
        "ngo"
    )

    create_user(
        "Demo Volunteer",
        "volunteer@example.com",
        "Volunteer@123",
        "volunteer"
    )

    create_user(
        "System Admin",
        "admin@example.com",
        "Admin@123",
        "admin"
    )

    db.session.commit()

    print("Seed completed.")