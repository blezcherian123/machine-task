import random


def determine_match(boy_name, girl_name):
    """Pick a match result at random using Python's random library.

    Returns a clean result with a short match/not-match message.
    """
    is_match = random.choice([True, False])

    if is_match:
        message = f"{boy_name} & {girl_name} are a match"
    else:
        message = f"{boy_name} & {girl_name} are not a match"

    return {"is_match": is_match, "message": message}
