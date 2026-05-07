from collections import defaultdict
import re


COMMON_ITEMS = {

    "salt",
    "water",
    "oil",
    "rice",
    "sugar",
    "ghee",
    "wheat flour",
    "maida",
    "coffee powder",
    "tea powder",
    "milk",
    "curd",
    "butter",
    "besan",
    "rava"
}


def parse_ingredients(text):

    ingredients = []

    items = text.split(";")

    for item in items:

        if ":" in item:

            name, qty = item.split(":")

            ingredients.append(
                (
                    name.strip(),
                    qty.strip()
                )
            )

    return ingredients


def split_quantity(qty_text):

    """
    Converts:
    100g -> (100, g)
    500ml -> (500, ml)
    2 -> (2, count)
    """

    match = re.match(
        r"(\d+)\s*([a-zA-Z]*)",
        qty_text
    )

    if match:

        value = int(match.group(1))

        unit = match.group(2)

        if unit == "":
            unit = "count"

        return value, unit

    return 0, "count"


def generate_shopping_list(meal_plan):

    shopping = defaultdict(
        lambda: defaultdict(int)
    )

    for meal_name, dishes in meal_plan.items():

        for dish_type, dish in dishes.items():

            if dish is None:
                continue

            ingredients = parse_ingredients(
                dish["ingredients"]
            )

            for ingredient, qty in ingredients:

                ingredient_lower = ingredient.lower()

                if ingredient_lower not in COMMON_ITEMS:

                    value, unit = split_quantity(qty)

                    shopping[ingredient][unit] += value

    return shopping