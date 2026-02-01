from typing import List
import math


def face_distance_to_confidence(
    face_distance: float,
    threshold: float = 0.6
) -> float:

    if face_distance > threshold:
        # Linear falloff for non-matches
        range_val = 1.0 - threshold
        linear_val = (1.0 - face_distance) / (range_val * 2.0)
        return round(max(0.0, linear_val), 2)

    # Non-linear boost for strong matches
    range_val = threshold
    linear_val = 1.0 - (face_distance / (range_val * 2.0))
    confidence = linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

    return round(min(confidence, 1.0), 2)
