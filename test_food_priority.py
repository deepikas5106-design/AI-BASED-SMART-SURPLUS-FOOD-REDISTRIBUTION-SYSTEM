import pytest

from app import create_app
from extensions import db
from ml.predict import predict_food_priority


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


def test_predict_food_priority_for_critical_food():
    result = predict_food_priority(
        expiry_hours=2,
        quantity=10,
        food_type="cooked",
        donation_age_hours=1,
        storage_condition="refrigerated",
        food_category="non_vegetarian"
    )

    assert result["success"] is True
    assert result["priority"] in {"High", "Critical"}
    assert 0 <= float(result["confidence"]) <= 1


def test_food_priority_prediction_api(client):
    response = client.post(
        "/api/food-priority/predict",
        json={
            "expiry_hours": 4,
            "quantity": 10,
            "food_type": "cooked",
            "donation_age_hours": 1,
            "storage_condition": "refrigerated",
            "food_category": "non_vegetarian"
        }
    )

    assert response.status_code == 200, response.get_data(as_text=True)
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["priority"] in {"Low", "Medium", "High", "Critical"}
    assert 0 <= float(payload["confidence"]) <= 1


def test_food_priority_invalid_input():
    result = predict_food_priority(
        expiry_hours=-1,
        quantity=-2,
        food_type="",
        donation_age_hours=None,
        storage_condition=None,
        food_category=None
    )

    assert result["success"] is False
    assert "error" in result
