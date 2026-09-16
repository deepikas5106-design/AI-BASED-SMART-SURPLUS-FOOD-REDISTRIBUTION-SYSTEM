from pathlib import Path

import joblib
import pandas as pd

from ml.train_model import FEATURE_COLUMNS, train_and_save_model

MODEL_PATH = Path(__file__).resolve().parent / "food_priority_model.pkl"

FOOD_TYPE_ALIASES = {
    "cooked food": "cooked",
    "cooked": "cooked",
    "prepared food": "prepared food",
    "prepared": "prepared food",
    "milk": "milk",
    "dairy": "milk",
    "meat": "meat",
    "seafood": "seafood",
    "salad": "salad",
    "fruits": "fruits",
    "fruit": "fruits",
    "vegetables": "vegetables",
    "vegetable": "vegetables",
    "bakery": "bakery",
    "bread": "bakery",
    "cakes": "bakery",
    "packaged": "packaged",
    "packet": "packaged",
    "rice": "rice",
    "grain": "grain",
    "dry food": "dry food",
    "lentils": "lentils",
    "food": "packaged",
}

STORAGE_ALIASES = {
    "refrigerated": "refrigerated",
    "cold": "refrigerated",
    "frozen": "frozen",
    "room temperature": "room_temperature",
    "room_temp": "room_temperature",
    "room_temperature": "room_temperature",
    "dry": "dry",
    "ambient": "room_temperature",
    "normal": "room_temperature",
}

CATEGORY_ALIASES = {
    "non vegetarian": "non_vegetarian",
    "non_vegetarian": "non_vegetarian",
    "vegetarian": "vegetarian",
    "dairy": "dairy",
    "bakery": "bakery",
    "packaged": "packaged",
    "grain": "grain",
    "rice": "grain",
    "fruit": "vegetarian",
    "fruits": "vegetarian",
    "vegetables": "vegetarian",
    "cooked": "non_vegetarian",
    "prepared food": "non_vegetarian",
    "meat": "non_vegetarian",
    "seafood": "non_vegetarian",
    "milk": "dairy",
"lentils": "grain",
}


def normalize_food_type(value):
    if value is None:
        return "packaged"
    cleaned = str(value).strip().lower()
    return FOOD_TYPE_ALIASES.get(cleaned, cleaned)


def normalize_storage_condition(value):
    if value is None:
        return "room_temperature"
    cleaned = str(value).strip().lower().replace(" ", "_")
    return STORAGE_ALIASES.get(cleaned, cleaned)


def infer_food_category(food_type, provided_value=None):
    if provided_value is not None:
        cleaned = str(provided_value).strip().lower().replace(" ", "_")
        return CATEGORY_ALIASES.get(cleaned, cleaned)

    normalized = normalize_food_type(food_type)
    return CATEGORY_ALIASES.get(normalized, "packaged")


def load_model():
    if not MODEL_PATH.exists():
        train_and_save_model()
    payload = joblib.load(MODEL_PATH)
    return payload["model"]


def predict_food_priority(
    expiry_hours,
    quantity,
    food_type,
    donation_age_hours,
    storage_condition=None,
    food_category=None,
):
    try:
        expiry_value = float(expiry_hours)
        quantity_value = float(quantity)
        age_value = float(donation_age_hours)
    except (TypeError, ValueError):
        return {
            "success": False,
            "error": "expiry_hours, quantity, and donation_age_hours must be numeric values.",
        }

    if expiry_value <= 0:
        return {
            "success": False,
            "error": "expiry_hours must be greater than 0.",
        }

    if quantity_value <= 0:
        return {
            "success": False,
            "error": "quantity must be greater than 0.",
        }

    if age_value < 0:
        return {
            "success": False,
            "error": "donation_age_hours cannot be negative.",
        }

    if not food_type or not str(food_type).strip():
        return {
            "success": False,
            "error": "food_type is required.",
        }

    normalized_food_type = normalize_food_type(food_type)
    normalized_storage_condition = normalize_storage_condition(storage_condition)
    normalized_food_category = infer_food_category(normalized_food_type, food_category)

    record = pd.DataFrame([
        {
            "expiry_hours": expiry_value,
            "quantity": quantity_value,
            "food_type": normalized_food_type,
            "donation_age_hours": age_value,
            "storage_condition": normalized_storage_condition,
            "food_category": normalized_food_category,
        }
    ])

    if list(record.columns) != FEATURE_COLUMNS:
        record = record[FEATURE_COLUMNS]

    model = load_model()
    prediction = model.predict(record)[0]
    probabilities = model.predict_proba(record)[0]
    max_index = int(probabilities.argmax())
    confidence = float(probabilities[max_index])

    return {
        "success": True,
        "priority": str(prediction).title(),
        "confidence": round(confidence, 4),
        "probabilities": {
            label: round(float(val), 4)
            for label, val in zip(model.classes_, probabilities)
        },
    }


if __name__ == "__main__":
    print(predict_food_priority(
        expiry_hours=4,
        quantity=10,
        food_type="cooked",
        donation_age_hours=1,
        storage_condition="refrigerated",
        food_category="non_vegetarian",
    ))
