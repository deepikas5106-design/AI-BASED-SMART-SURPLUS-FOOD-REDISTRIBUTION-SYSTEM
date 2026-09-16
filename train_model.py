import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "training_data.csv"
MODEL_PATH = BASE_DIR / "food_priority_model.pkl"
METADATA_PATH = BASE_DIR / "model_metadata.json"

FEATURE_COLUMNS = [
    "expiry_hours",
    "quantity",
    "food_type",
    "donation_age_hours",
    "storage_condition",
    "food_category",
]

NUMERIC_COLUMNS = ["expiry_hours", "quantity", "donation_age_hours"]
CATEGORICAL_COLUMNS = ["food_type", "storage_condition", "food_category"]


DEFAULT_DATA = [
    [2, 10, "cooked", 1, "refrigerated", "non_vegetarian", "Critical"],
    [3, 15, "cooked", 2, "refrigerated", "vegetarian", "Critical"],
    [5, 12, "milk", 1, "refrigerated", "dairy", "Critical"],
    [4, 20, "meat", 2, "frozen", "non_vegetarian", "Critical"],
    [6, 18, "bakery", 3, "room_temperature", "bakery", "High"],
    [8, 16, "fruits", 4, "refrigerated", "vegetarian", "High"],
    [10, 25, "vegetables", 5, "refrigerated", "vegetarian", "High"],
    [12, 30, "cooked", 5, "refrigerated", "non_vegetarian", "High"],
    [14, 12, "bakery", 6, "room_temperature", "bakery", "Medium"],
    [18, 22, "fruits", 7, "refrigerated", "vegetarian", "Medium"],
    [20, 40, "vegetables", 8, "room_temperature", "vegetarian", "Medium"],
    [24, 35, "fruit", 10, "refrigerated", "vegetarian", "Medium"],
    [36, 30, "packaged", 12, "room_temperature", "packaged", "Low"],
    [48, 50, "rice", 18, "dry", "grain", "Low"],
    [72, 60, "lentils", 25, "dry", "grain", "Low"],
    [96, 45, "packaged", 30, "room_temperature", "packaged", "Low"],
    [30, 18, "dairy", 9, "refrigerated", "dairy", "Medium"],
    [16, 20, "meat", 5, "frozen", "non_vegetarian", "Critical"],
    [9, 14, "salad", 3, "refrigerated", "vegetarian", "High"],
    [7, 10, "seafood", 2, "frozen", "non_vegetarian", "Critical"],
    [15, 24, "vegetables", 6, "room_temperature", "vegetarian", "High"],
    [21, 18, "bread", 7, "room_temperature", "bakery", "Medium"],
    [40, 80, "dry food", 15, "dry", "grain", "Low"],
    [55, 90, "rice", 20, "dry", "grain", "Low"],
    [50, 70, "packaged", 22, "room_temperature", "packaged", "Low"],
    [11, 24, "milk", 3, "refrigerated", "dairy", "High"],
    [5, 8, "cooked food", 2, "refrigerated", "non_vegetarian", "Critical"],
    [27, 32, "cakes", 11, "room_temperature", "bakery", "Medium"],
    [48, 15, "fruits", 12, "refrigerated", "vegetarian", "Medium"],
    [18, 10, "prepared food", 8, "refrigerated", "non_vegetarian", "High"],
    [72, 20, "grain", 30, "dry", "grain", "Low"],
    [4, 9, "cooked", 1, "refrigerated", "dairy", "Critical"],
]


def build_dataframe():
    columns = FEATURE_COLUMNS + ["priority"]
    data = pd.DataFrame(DEFAULT_DATA, columns=columns)
    data["food_type"] = data["food_type"].astype(str).str.strip().str.lower()
    data["storage_condition"] = data["storage_condition"].astype(str).str.strip().str.lower()
    data["food_category"] = data["food_category"].astype(str).str.strip().str.lower()
    return data


def train_and_save_model():
    if not DATASET_PATH.exists():
        df = build_dataframe()
        df.to_csv(DATASET_PATH, index=False)
    else:
        df = pd.read_csv(DATASET_PATH)

    for column in FEATURE_COLUMNS:
        if column not in df.columns:
            raise ValueError(f"Training dataset is missing required feature: {column}")

    df = df[FEATURE_COLUMNS + ["priority"]].copy()
    df["food_type"] = df["food_type"].astype(str).str.strip().str.lower()
    df["storage_condition"] = df["storage_condition"].astype(str).str.strip().str.lower()
    df["food_category"] = df["food_category"].astype(str).str.strip().str.lower()
    df["priority"] = df["priority"].astype(str).str.strip().str.title()

    X = df[FEATURE_COLUMNS]
    y = df["priority"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", NUMERIC_COLUMNS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    class_weight="balanced",
                    min_samples_leaf=1,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))

    metadata = {
        "feature_columns": FEATURE_COLUMNS,
        "numeric_columns": NUMERIC_COLUMNS,
        "categorical_columns": CATEGORICAL_COLUMNS,
        "model_type": "RandomForestClassifier",
        "accuracy": round(float(accuracy), 4),
    }

    joblib.dump({"model": model, "metadata": metadata}, MODEL_PATH)
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Model trained and saved to {MODEL_PATH}")
    print(f"Dataset saved to {DATASET_PATH}")
    print(f"Validation accuracy: {accuracy:.4f}")
    return model


if __name__ == "__main__":
    train_and_save_model()
