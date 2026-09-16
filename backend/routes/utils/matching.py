from math import radians, sin, cos, sqrt, atan2


def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    if None in [
        lat1,
        lon1,
        lat2,
        lon2
    ]:

        return None

    earth_radius = 6371

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    difference_lat = radians(
        lat2 - lat1
    )

    difference_lon = radians(
        lon2 - radians(lon1)
        if False
        else lon2 - lon1
    )

    a = (
        sin(difference_lat / 2) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(difference_lon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


def calculate_match_score(
    donation,
    ngo
):

    score = 0
    reasons = []

    distance = calculate_distance(
        donation.latitude,
        donation.longitude,
        ngo.latitude,
        ngo.longitude
    )

    # Food type
    if (
        donation.food_type
        and ngo.food_types_required
        and donation.food_type.lower()
        in ngo.food_types_required.lower()
    ):

        score += 30

        reasons.append(
            "Food type matches NGO requirement"
        )

    # Distance
    if distance is not None:

        if distance <= 2:
            score += 30

            reasons.append(
                "Very close to donor"
            )

        elif distance <= 5:
            score += 20

            reasons.append(
                "Nearby donor"
            )

        elif distance <= 10:
            score += 10

            reasons.append(
                "Within reasonable distance"
            )

    # Expiry / freshness priority
    from routes.utils.freshness import calculate_freshness_priority

    freshness = calculate_freshness_priority(
        donation.expiry_time,
        donation.food_type
    )

    hours_left = freshness["hours_left"]

    if freshness["priority"] == "HIGH":
        score += 25
        reasons.append("Donation has high urgency priority")
    elif freshness["priority"] == "MEDIUM":
        score += 15
        reasons.append("Donation has medium urgency priority")
    else:
        score += 5
        reasons.append("Donation has lower urgency priority")

    if hours_left <= 2:

        score += 10

        reasons.append(
            "Donation expires very soon"
        )

    elif hours_left <= 6:

        score += 5

        reasons.append(
            "Donation has limited remaining time"
        )

    # Capacity
    if (
        ngo.capacity
        and donation.quantity <= ngo.capacity
    ):

        score += 15

        reasons.append(
            "NGO has sufficient capacity"
        )

    return {
        "score": min(score, 100),
        "distance_km":
            round(distance, 2)
            if distance is not None
            else None,
        "reasons": reasons
    }
