def calculate_bmr(age, sex, weight, height):
    """
    Calculate Basal Metabolic Rate (BMR)
    using the Mifflin-St Jeor equation.
    """

    if sex == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif sex == "Female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        raise ValueError("Sex must be 'Male' or 'Female'.")

    return round(bmr)


def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure (TDEE)
    using an activity multiplier.
    """

    activity_level = activity_level.lower().strip()

    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }

    if activity_level not in activity_multipliers:
        raise ValueError(
            "Invalid activity level."
        )

    tdee = bmr * activity_multipliers[activity_level]

    return round(tdee)


def calculate_calorie_target(tdee, goal):
    """
    Calculate daily calorie target based on the user's goal.
    """

    goal = goal.lower().strip()

    if goal in ["lose", "lose weight"]:
        calorie_target = tdee - 500

    elif goal in ["maintain", "maintain weight"]:
        calorie_target = tdee

    elif goal in ["gain", "gain weight"]:
        calorie_target = tdee + 500

    else:
        raise ValueError(
            "Invalid goal."
        )

    return max(round(calorie_target), 1200)


def calculate_macros(calorie_target, weight):
    """
    Calculate approximate daily macronutrient targets.

    Protein: 1.6 g per kg body weight
    Fat: 25% of daily calories
    Carbohydrates: remaining calories
    """

    protein = round(weight * 1.6)

    fat = round((calorie_target * 0.25) / 9)

    protein_calories = protein * 4
    fat_calories = fat * 9

    remaining_calories = (
        calorie_target
        - protein_calories
        - fat_calories
    )

    carbs = max(round(remaining_calories / 4), 0)

    return {
        "protein": protein,
        "carbs": carbs,
        "fat": fat
    }