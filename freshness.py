from datetime import datetime, timezone


PERISHABLE_FOOD_TYPES = {
    "cooked food",
    "bakery items",
    "fruits",
    "vegetables",
    "milk",
    "dairy",
    "meat",
    "seafood",
    "salad",
    "prepared food"
}


def calculate_freshness_priority(expiry_time, food_type=None, current_time=None):
    if expiry_time is None:
        return {
            "priority": "LOW",
            "freshness_score": 0,
            "hours_left": 0,
            "reason": "No expiry date provided"
        }

    if current_time is None:
        current_time = datetime.now(timezone.utc)

    if expiry_time.tzinfo is None:
        expiry_time = expiry_time.replace(tzinfo=timezone.utc)

    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)

    hours_left = max(0.0, (expiry_time - current_time).total_seconds() / 3600)

    type_key = (food_type or "").strip().lower()
    urgency_bonus = 10 if type_key in PERISHABLE_FOOD_TYPES else 0

    if hours_left <= 6:
        priority = "HIGH"
        score = 90 + urgency_bonus
        reason = "Food expires within a few hours and needs urgent redistribution."
    elif hours_left <= 24:
        priority = "MEDIUM"
        score = 75 + urgency_bonus
        reason = "Food expires within the next day and should be prioritized soon."
    else:
        priority = "LOW"
        score = 45 + urgency_bonus
        reason = "Food has several days remaining before expiry."

    score = max(0, min(100, int(round(score))))

    return {
        "priority": priority,
        "freshness_score": score,
        "hours_left": round(hours_left, 2),
        "reason": reason,
        "food_type": food_type or "Unknown"
    }
