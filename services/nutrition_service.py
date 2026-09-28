import pandas as pd
from pathlib import Path
import math
import re


# Path to the nutrition dataset
data_path = Path(__file__).parent.parent / "data" / "nutrition.csv"


def load_nutrition_data():
    """Load the nutrition dataset from CSV."""
    return pd.read_csv(data_path)


def find_food(food_name):
    """
    Find a food in the nutrition dataset by dish name.
    Returns the nutrition information if found.
    """

    df = load_nutrition_data()
    # Clean dish names for easier matching
    df["Dish Name"] = df["Dish Name"].astype(str).str.strip()
    food_name = food_name.strip().lower()
    # Exact match first
    exact_match = df[
        df["Dish Name"].str.lower() == food_name
    ]
    if not exact_match.empty:
        return exact_match.iloc[0].to_dict()
    # Partial match if exact match is not found
    partial_match = df[
        df["Dish Name"].str.lower().str.contains(
            food_name,
            na=False
        )
    ]
    if not partial_match.empty:
        return partial_match.iloc[0].to_dict()

    return None


def search_foods(food_name, limit=15):
    """
    Search the nutrition database for possible food matches.
    Returns up to 'limit' matching foods.
    """
    df = load_nutrition_data()
    df["Dish Name"] = (
        df["Dish Name"]
        .astype(str)
        .str.strip()
    )

    food_name = food_name.strip().lower()
    # 1. Exact match
    exact_match = df[
        df["Dish Name"].str.lower() == food_name
    ]
    if not exact_match.empty:
        exact_records = exact_match.to_dict("records")
    else:
        exact_records = []

    # 2. Phrase/partial match
    partial_match = df[
        df["Dish Name"]
        .str.lower()
        .str.contains(food_name, na=False)
    ]
    if not partial_match.empty:
        partial_records = partial_match.to_dict("records")
    else:
        partial_records = []

    # 3. Match using individual meaningful words
    words = [
        word for word in food_name.split()
        if len(word) > 2
    ]
    if not words:
        return []

    # Score each dish based on how many search words occur
    def calculate_match_score(dish_name):
            dish_name = str(dish_name).lower()
            return sum(word in dish_name for word in words)

    df["match_score"] = (
        df["Dish Name"]
        .apply(calculate_match_score)
    )

    matches = df[
        df["match_score"] > 0
    ].sort_values(
        by="match_score",
        ascending=False
    )

    word_records = matches.drop(
        columns=["match_score"]
    ).to_dict("records")

    # Combine all matching results
    all_records = exact_records + partial_records + word_records

    # Remove duplicate dishes
    unique_records = []
    seen_names = set()

    for record in all_records:
        dish_name = record["Dish Name"]

        if dish_name not in seen_names:
            unique_records.append(record)
            seen_names.add(dish_name)

    # Rank results by relevance to the search query
    def relevance_score(record):
        dish_name = str(record["Dish Name"]).lower()

        # Exact match gets the highest priority
        if dish_name == food_name:
            return 1000

        # Full phrase match gets very high priority
        if food_name in dish_name:
            return 500

        score = 0

        # The first search word is treated as the primary food keyword
        primary_word = words[0]

        # Primary food keyword gets much higher importance
        if re.search(
            r"\b" + re.escape(primary_word) + r"\b",
            dish_name
        ):
            score += 100
            # Give extra priority when the primary food
            # appears at the beginning of the dish name
            if dish_name.startswith(primary_word):
                score += 20

        # Secondary words receive lower importance
        for word in words[1:]:
            if re.search(
                r"\b" + re.escape(word) + r"\b",
                dish_name
            ):
                score += 10

        return score

    unique_records.sort(
        key=relevance_score,
        reverse=True
    )

    return unique_records[:limit]


def calculate_portion_nutrition(food_data, portion_grams):
    """
    Calculate nutrition values based on the user's portion size.
    The nutrition dataset is assumed to provide values per 100g.
    """

    factor = portion_grams / 100

    nutrition = {
        "Calories": food_data["Calories (kcal)"] * factor,
        "Protein": food_data["Protein (g)"] * factor,
        "Carbohydrates": food_data["Carbohydrates (g)"] * factor,
        "Fat": food_data["Fats (g)"] * factor,
        "Fibre": food_data["Fibre (g)"] * factor,
        "Free Sugar": food_data["Free Sugar (g)"] * factor,
        "Sodium": food_data["Sodium (mg)"] * factor,
        "Calcium": food_data["Calcium (mg)"] * factor,
        "Iron": food_data["Iron (mg)"] * factor,
        "Vitamin C": food_data["Vitamin C (mg)"] * factor,
        "Folate": food_data["Folate (µg)"] * factor
    }

    return nutrition



def compare_with_daily_targets(nutrition, calorie_target, macro_targets):
    """
    Compare a meal's nutrition with the user's daily targets.
    Returns the percentage of each daily target consumed.
    """

    comparison = {
        "Calories": round(
            (nutrition["Calories"] / calorie_target) * 100, 1
        ),
        "Protein": round(
            (nutrition["Protein"] / macro_targets["protein"]) * 100, 1
        ),
        "Carbohydrates": round(
            (nutrition["Carbohydrates"] / macro_targets["carbs"]) * 100, 1
        ),
        "Fat": round(
            (nutrition["Fat"] / macro_targets["fat"]) * 100, 1
        )
    }

    return comparison