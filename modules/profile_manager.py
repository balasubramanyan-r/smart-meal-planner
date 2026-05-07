import json

PROFILE_FILE = "user_profile.json"

def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f)

def load_profile():
    try:
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def detect_food_type(preferences):

    nonveg_items = [
        "chicken",
        "mutton",
        "fish",
        "egg",
        "prawn"
    ]

    for item in preferences:

        item_lower = item.lower()

        for nv in nonveg_items:

            if nv in item_lower:
                return "Non-Vegetarian"

    return "Vegetarian"