import pandas as pd
from pathlib import Path


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