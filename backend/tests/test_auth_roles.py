import pytest

from app import create_app
from extensions import db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()


def test_individual_role_is_accepted(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test Individual",
            "email": "individual@test.com",
            "password": "TestPass123",
            "role": "individual"
        },
    )

    assert response.status_code == 201, response.get_data(as_text=True)
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["role"] == "donor"
