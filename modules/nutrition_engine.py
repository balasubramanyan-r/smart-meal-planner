
def calculate_meal_nutrition(meal):

    totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    for dish_type, dish in meal.items():

        if dish is None:
            continue

        totals["calories"] += float(
            dish.get("calories", 0)
        )

        totals["protein"] += float(
            dish.get("protein", 0)
        )

        totals["carbs"] += float(
            dish.get("carbs", 0)
        )

        totals["fat"] += float(
            dish.get("fat", 0)
        )

    return totals



def calculate_day_nutrition(meal_plan):

    day_totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    meal_wise = {}

    for meal_name, meal in meal_plan.items():

        meal_totals = calculate_meal_nutrition(meal)

        meal_wise[meal_name] = meal_totals

        day_totals["calories"] += meal_totals["calories"]
        day_totals["protein"] += meal_totals["protein"]
        day_totals["carbs"] += meal_totals["carbs"]
        day_totals["fat"] += meal_totals["fat"]

    return meal_wise, day_totals