import streamlit as st
from datetime import datetime

from modules.profile_manager import (
    detect_food_type
)

from modules.recommender import (
    recommend_full_meal
)

from modules.ingredient_engine import (
    generate_shopping_list
)

from modules.nutrition_engine import (
    calculate_day_nutrition
)

from modules.database import (
    create_tables,
    create_profile,
    get_profiles
)

from modules.auth import (
    register_user,
    login_user
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Meal Planner",
    layout="wide"
)

create_tables()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = None


# =========================================================
# TITLE
# =========================================================

st.title("🍲 Smart Meal Planner Bot")


# =========================================================
# SIDEBAR ACCOUNT SECTION
# =========================================================

st.sidebar.header("Account")

if not st.session_state.logged_in:

    auth_mode = st.sidebar.radio(
        "Select",
        ["Login", "Register"]
    )

    email = st.sidebar.text_input("Email")

    password = st.sidebar.text_input(
        "Password",
        type="password"
    )

    # =====================================================
    # REGISTER
    # =====================================================

    if auth_mode == "Register":

        if st.sidebar.button("Create Account"):

            success = register_user(
                email,
                password
            )

            if success:

                st.sidebar.success(
                    "Account created!"
                )

            else:

                st.sidebar.error(
                    "Email already exists"
                )

    # =====================================================
    # LOGIN
    # =====================================================

    else:

        if st.sidebar.button("Login"):

            account = login_user(
                email,
                password
            )

            if account:

                st.session_state.logged_in = True

                st.session_state.account = account

                st.rerun()

            else:

                st.sidebar.error(
                    "Invalid credentials"
                )

else:

    st.sidebar.success(
        f"Logged in as:\n"
        f"{st.session_state.account[1]}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.account = None

        st.session_state.selected_profile = None

        st.rerun()


# =========================================================
# MAIN APP
# =========================================================

if st.session_state.logged_in:

    account_id = st.session_state.account[0]

    # =====================================================
    # LOAD PROFILES
    # =====================================================

    profiles = get_profiles(account_id)

    st.sidebar.header("Profiles")

    # =====================================================
    # PROFILE SELECTION
    # =====================================================

    if profiles:

        profile_names = [
            p[2]
            for p in profiles
        ]

        selected_name = st.sidebar.selectbox(
            "Select Profile",
            profile_names
        )

        selected_profile = next(
            p for p in profiles
            if p[2] == selected_name
        )

        st.session_state.selected_profile = (
            selected_profile
        )

    else:

        st.sidebar.warning(
            "No profiles created yet."
        )

    # =====================================================
    # CREATE PROFILE SECTION
    # =====================================================

    with st.sidebar.expander(
        "➕ Create New Profile"
    ):

        with st.form("create_profile_form"):

            profile_name = st.text_input(
                "Profile Name"
            )

            profile_location = st.selectbox(
                "Location",
                [
                    "Tamil Nadu",
                    "Kerala",
                    "Karnataka",
                    "Andhra Pradesh",
                    "India"
                ]
            )

            preferred_foods = st.text_area(
                "Preferred Foods"
            )

            avoided_foods = st.text_area(
                "Foods To Avoid"
            )

            create_profile_button = (
                st.form_submit_button(
                    "Create Profile"
                )
            )

            if create_profile_button:

                preferred_list = [

                    x.strip()

                    for x in preferred_foods.split(",")

                    if x.strip()
                ]

                food_type = detect_food_type(
                    preferred_list
                )

                create_profile(
                    account_id,
                    profile_name,
                    profile_location,
                    food_type,
                    preferred_foods,
                    avoided_foods
                )

                st.success(
                    "Profile Created!"
                )

                st.rerun()

    # =====================================================
    # STOP IF NO PROFILE SELECTED
    # =====================================================

    if st.session_state.selected_profile is None:

        st.warning(
            "Please create and select a profile."
        )

        st.stop()

    # =====================================================
    # PROFILE DATA
    # =====================================================

    selected_profile = (
        st.session_state.selected_profile
    )

    profile_name = selected_profile[2]

    location = selected_profile[3]

    food_type = selected_profile[4]

    preferred_foods = selected_profile[5]

    avoided_foods = selected_profile[6]

    veg = food_type == "Vegetarian"

    # =====================================================
    # PROFILE DISPLAY
    # =====================================================

    st.subheader(f"Welcome {profile_name}")

    st.write(f"Food Type: {food_type}")

    st.write(f"Location: {location}")

    st.write(
        f"Preferred Foods: {preferred_foods}"
    )

    st.write(
        f"Foods To Avoid: {avoided_foods}"
    )

    preferred_list = [

        x.strip()

        for x in preferred_foods.split(",")

        if x.strip()
    ]

    avoid_list = [

        x.strip()

        for x in avoided_foods.split(",")

        if x.strip()
    ]

    # =====================================================
    # MEAL GENERATION
    # =====================================================

    today = datetime.now()

    weekend = today.weekday() >= 5

    meal_plan = {

        "Breakfast": recommend_full_meal(
            "Breakfast",
            location,
            veg,
            weekend,
            avoid_list,
            preferred_list
        ),

        "Lunch": recommend_full_meal(
            "Lunch",
            location,
            veg,
            weekend,
            avoid_list,
            preferred_list
        ),

        "Snacks": recommend_full_meal(
            "Snacks",
            location,
            veg,
            weekend,
            avoid_list,
            preferred_list
        ),

        "Dinner": recommend_full_meal(
            "Dinner",
            location,
            veg,
            weekend,
            avoid_list,
            preferred_list
        )
    }

    # =====================================================
    # NUTRITION
    # =====================================================

    meal_nutrition, day_nutrition = \
        calculate_day_nutrition(
            meal_plan
        )

    # =====================================================
    # DISPLAY MEALS
    # =====================================================

    st.header("Today's Meal Plan")

    for meal_name, dishes in meal_plan.items():

        st.subheader(meal_name)

        for dish_type, dish in dishes.items():

            if dish:

                st.write(
                    f"🍽️ {dish_type}: "
                    f"{dish['dish_name']}"
                )

                st.write(
                    f"🧂 {dish['ingredients']}"
                )

        nutrition = meal_nutrition[meal_name]

        st.info(
            f"🔥 Calories: "
            f"{nutrition['calories']} kcal | "

            f"💪 Protein: "
            f"{nutrition['protein']} g | "

            f"🍚 Carbs: "
            f"{nutrition['carbs']} g | "

            f"🧈 Fat: "
            f"{nutrition['fat']} g"
        )

    # =====================================================
    # SHOPPING LIST
    # =====================================================

    st.header(
        "Tomorrow's Ingredients To Buy"
    )

    shopping = generate_shopping_list(
        meal_plan
    )

    for item, unit_data in shopping.items():

        qty_strings = []

        for unit, value in unit_data.items():

            if unit == "count":

                qty_strings.append(
                    f"{value}"
                )

            else:

                qty_strings.append(
                    f"{value}{unit}"
                )

        st.write(
            f"🛒 {item}: "
            f"{', '.join(qty_strings)}"
        )

    # =====================================================
    # DAY NUTRITION
    # =====================================================

    st.header(
        "📊 Full Day Nutrition Summary"
    )

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