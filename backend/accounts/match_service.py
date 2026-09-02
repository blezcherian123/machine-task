import random


def determine_match(boy_name, girl_name):
    """Determine match result based on names."""

    # Special match condition
    if boy_name.strip().lower() == "bachan" and girl_name.strip().lower() == "aash":
        is_match = True
        message = f"{boy_name} & {girl_name} are a match"
        special_message = "Made for Each Other...!!!!"

        return {
            "is_match": is_match,
            "message": message,
            "special_message": special_message,
        }

    # Default random result for other names
    is_match = random.choice([True, False])

    if is_match:
        message = f"{boy_name} & {girl_name} are a match"
    else:
        message = f"{boy_name} & {girl_name} are not a match"

    return {
        "is_match": is_match,
        "message": message,
    }