import pandas as pd
import random
from datetime import datetime, timedelta

recipes = pd.read_csv(
    "recipes_full.csv",
    encoding="utf-8-sig"
)

recipes.columns = recipes.columns.str.strip()

HISTORY_FILE = "meal_history.csv"


def load_history():
    try:
        return pd.read_csv(HISTORY_FILE)
    except:
        return pd.DataFrame()

def save_history(data):
    data.to_csv(HISTORY_FILE, index=False)

def get_recent_dishes(days=15):

    history = load_history()

    if history.empty:
        return []

    cutoff = datetime.now() - timedelta(days=days)

    history["date"] = pd.to_datetime(history["date"])

    recent = history[history["date"] >= cutoff]

    used = []

    for col in history.columns:
        if col != "date":
            used.extend(
                recent[col].dropna().tolist()
            )

    return used


def choose_dish(
    meal_category,
    dish_type,
    region,
    veg=True,
    weekend=False
):

    filtered = recipes[
        (recipes["meal_category"] == meal_category)
        &
        (recipes["dish_type"] == dish_type)
    ]

    if veg:
        filtered = filtered[
            filtered["veg"] == True
        ]

    regional_filtered = filtered[
        filtered["region"].str.contains(
            region,
            case=False,
            na=False
        )
    ]

    if len(regional_filtered) > 0:
        filtered = regional_filtered

    recent = get_recent_dishes()

    filtered = filtered[
        ~filtered["dish_name"].isin(recent)
    ]

    if weekend:
        special = filtered[
            filtered["weekend_special"] == True
        ]

        if len(special) > 0:
            filtered = special

    if len(filtered) == 0:
        return None

    return random.choice(
        filtered.to_dict("records")
    )


def recommend_full_meal(
    meal_category,
    region,
    veg=True,
    weekend=False
):

    meal = {}

    if meal_category == "Breakfast":

        meal["Main"] = choose_dish(
            "Breakfast",
            "Main",
            region,
            veg,
            weekend
        )

        meal["Side"] = choose_dish(
            "Breakfast",
            "Side",
            region,
            veg,
            weekend
        )

        meal["Beverage"] = choose_dish(
            "Breakfast",
            "Beverage",
            region,
            veg,
            weekend
        )

    elif meal_category == "Lunch":

        meal["Main"] = choose_dish(
            "Lunch",
            "Main",
            region,
            veg,
            weekend
        )

        meal["Gravy"] = choose_dish(
            "Lunch",
            "Gravy",
            region,
            veg,
            weekend
        )

        meal["Side"] = choose_dish(
            "Lunch",
            "Side",
            region,
            veg,
            weekend
        )

        meal["Extra"] = choose_dish(
            "Lunch",
            "Extra",
            region,
            veg,
            weekend
        )

    elif meal_category == "Dinner":

        meal["Main"] = choose_dish(
            "Dinner",
            "Main",
            region,
            veg,
            weekend
        )

        meal["Side"] = choose_dish(
            "Dinner",
            "Side",
            region,
            veg,
            weekend
        )

    elif meal_category == "Snacks":

        meal["Snack"] = choose_dish(
            "Snacks",
            "Snacks",
            region,
            veg,
            weekend
        )

        meal["Beverage"] = choose_dish(
            "Snacks",
            "Beverage",
            region,
            veg,
            weekend
        )

    return meal