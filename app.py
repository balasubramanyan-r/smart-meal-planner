import streamlit as st
import pandas as pd
from datetime import datetime

from modules.profile_manager import (
    save_profile,
    load_profile,
    detect_food_type
)

from modules.recommender import (
    recommend_full_meal,
    load_history,
    save_history
)

from modules.ingredient_engine import (
    generate_shopping_list
)

from modules.nutrition_engine import (
    calculate_day_nutrition
)

st.set_page_config(
    page_title="Smart Meal Planner",
    layout="wide"
)

st.title("🍲 Smart Meal Planner Bot")

profile = load_profile()

st.sidebar.header("User Preferences")

name = st.sidebar.text_input("Name")

location = st.sidebar.selectbox(
    "Location",
    [
        "Tamil Nadu",
        "Karnataka",
        "Kerala",
        "Andhra Pradesh",
        "India"
    ]
)

preferred_items = st.sidebar.text_area(
    "Preferred Food Items (comma separated)"
)

if st.sidebar.button("Save Preferences"):

    items = [
        x.strip()
        for x in preferred_items.split(",")
    ]

    food_type = detect_food_type(items)

    profile = {
        "name": name,
        "location": location,
        "preferences": items,
        "food_type": food_type
    }

    save_profile(profile)

    st.success("Preferences Saved!")

if profile:

    st.subheader(f"Welcome {profile['name']}")

    st.write(f"Food Type: {profile['food_type']}")
    st.write(f"Location: {profile['location']}")

    today = datetime.now()

    weekend = today.weekday() >= 5

    veg = profile["food_type"] == "Vegetarian"

    meal_plan = {

        "Breakfast": recommend_full_meal(
            "Breakfast",
            profile["location"],
            veg,
            weekend
        ),

        "Lunch": recommend_full_meal(
            "Lunch",
            profile["location"],
            veg,
            weekend
        ),

        "Snacks": recommend_full_meal(
            "Snacks",
            profile["location"],
            veg,
            weekend
        ),

        "Dinner": recommend_full_meal(
            "Dinner",
            profile["location"],
            veg,
            weekend
        )

    }

    meal_nutrition, day_nutrition = \
        calculate_day_nutrition(meal_plan)

    st.header("Today's Meal Plan")

    for meal_name, dishes in meal_plan.items():

        st.subheader(meal_name)

        for dish_type, dish in dishes.items():
            nutrition = meal_nutrition[meal_name]

            if dish:
                st.write(
                    f"🍽️ {dish_type}: {dish['dish_name']}"
                )

                st.write(
                    f"🧂 {dish['ingredients']}"
                )

        st.info(
            f"🔥 Calories: {nutrition['calories']} kcal | "
            f"💪 Protein: {nutrition['protein']} g | "
            f"🍚 Carbs: {nutrition['carbs']} g | "
            f"🧈 Fat: {nutrition['fat']} g"
        )


    st.header("Tomorrow's Ingredients To Buy")

    shopping = generate_shopping_list(meal_plan)

    for item, unit_data in shopping.items():

        qty_strings = []

        for unit, value in unit_data.items():

            if unit == "count":
                qty_strings.append(f"{value}")
            else:
                qty_strings.append(f"{value}{unit}")

        st.write(
            f"🛒 {item}: {', '.join(qty_strings)}"
        )

    st.header("📊 Full Day Nutrition Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Calories",
            f"{day_nutrition['calories']} kcal"
        )

        st.metric(
            "Protein",
            f"{day_nutrition['protein']} g"
        )

    with col2:

        st.metric(
            "Carbohydrates",
            f"{day_nutrition['carbs']} g"
        )

        st.metric(
            "Fat",
            f"{day_nutrition['fat']} g"
        )

    if st.button("Save Today's Plan"):

        history = load_history()

        new_row = {
            "date": str(today.date()),
            "Breakfast": meals["Breakfast"]["recipe_name"],
            "Lunch": meals["Lunch"]["recipe_name"],
            "Snacks": meals["Snacks"]["recipe_name"],
            "Dinner": meals["Dinner"]["recipe_name"]
        }

        history = pd.concat(
            [
                history,
                pd.DataFrame([new_row])
            ],
            ignore_index=True
        )

        save_history(history)

        st.success("Meal Plan Saved!")