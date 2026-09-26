import streamlit as st
from database.db import initialize_database, save_profile, get_profile
from services.calorie_service import(
    calculate_bmr,
    calculate_tdee,
    calculate_calorie_target,
    calculate_macros
)
from services.nutrition_service import find_food

# Page configuration
st.set_page_config(
    page_title = "NutriSnap",
    page_icon = "🥗"
)
initialize_database()
saved_profile = get_profile()

# Sidebar
st.sidebar.title("🥗 NutriSnap")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "My Profile", "Meal Analysis", "History"]
)

# Home Page
if page == "Home":
    st.title("🥗 NutriSnap")
    st.subheader(
        "AI-Powered Personal Nutrition Assistant"
    )
    st.write(
        "Analyze your meals, understand their nutritional "
        "content, and receive personalized nutrition insights."
    )
    st.info(
        "Start by creating your nutrition profile."
    )

# Profile Page
elif page == "My Profile":
    st.title("👤 My Nutrition Profile")
    st.write(
        "Enter your information to estimate your daily "
        "calorie and macronutrient requirements."
    )
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(
            "Age",
            min_value=13,
            max_value=100,
            value= saved_profile[0] if saved_profile else 21,
            step=1
        )
        sex_options = ["Male", "Female"]
        sex = st.selectbox(
            "Sex",
            sex_options,
            index=sex_options.index(saved_profile[1]) 
            if saved_profile and saved_profile[1] in sex_options 
            else 0
        )
        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=250.0,
            value=float(saved_profile[2]) if saved_profile else 170.0,
            step=1.0
        )

    with col2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=300.0,
            value=float(saved_profile[3]) if saved_profile else 70.0,
            step=0.5
        )
        activity_options = [
                 "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active",
                "Extra Active"
                ]
        activity_level = st.selectbox(
            "Activity Level",
            activity_options,
            index=(
                activity_options.index(saved_profile[4])
                if saved_profile and saved_profile[4] in activity_options
                else 0
            )
        )
        goal_options = [
            "Lose Weight",
            "Maintain Weight",
            "Gain Weight"
        ]
        goal = st.selectbox(
            "Goal",
            goal_options,
            index=(
                goal_options.index(saved_profile[5])
                if saved_profile and saved_profile[5] in goal_options
                else 0
            )
        )
    if st.button("Calculate My Requirements"):

        bmr = calculate_bmr(
            age,
            sex,
            weight,
            height
        )
        tdee = calculate_tdee(
            bmr,
            activity_level
        )
        calorie_target = calculate_calorie_target(
            tdee,
            goal
        )
        macros = calculate_macros(
            calorie_target,
            weight
        )
        save_profile(
            age,
            sex,
            height,
            weight,
            activity_level,
            goal,
            bmr,
            tdee,
            calorie_target,
            macros["protein"],
            macros["carbs"],
            macros["fat"]
        )
        st.success("Your nutrition profile has been calculated!")
        st.subheader("📊 Your Daily Requirements")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "BMR",
                f"{bmr} kcal"
            )

        with col2:
            st.metric(
                "TDEE",
                f"{tdee} kcal"
            )

        with col3:
            st.metric(
                "Daily Calories",
                f"{calorie_target} kcal"
            )

        st.subheader("🥩 Daily Macronutrient Targets")
        macro1, macro2, macro3 = st.columns(3)
        with macro1:
            st.metric(
                "Protein",
                f"{macros['protein']} g"
            )
        with macro2:
            st.metric(
                "Carbohydrates",
                f"{macros['carbs']} g"
            )
        with macro3:
            st.metric(
                "Fat",
                f"{macros['fat']} g"
            )
        st.caption(
            "These values are estimates based on standard "
            "equations and should not be considered medical advice."
        )

# Meal Analysis Page
elif page == "Meal Analysis":

    st.title("🍽️ Meal Analysis")

    st.write(
        "Search for a food to view its nutritional information "
        "from the NutriSnap nutrition database."
    )

    food_name = st.text_input(
        "Enter a food or dish name",
        placeholder="Example: Chicken Biryani"
    )

    if st.button("Analyze Nutrition"):

        if not food_name.strip():

            st.warning("Please enter a food or dish name.")

        else:

            result = find_food(food_name)

            if result is None:

                st.error(
                    "Food not found in the nutrition database."
                )

            else:

                st.success(
                    f"Food found: {result['Dish Name']}"
                )

                st.subheader("📊 Nutrition Information")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Calories",
                        f"{result['Calories (kcal)']} kcal"
                    )

                with col2:
                    st.metric(
                        "Protein",
                        f"{result['Protein (g)']} g"
                    )

                with col3:
                    st.metric(
                        "Carbohydrates",
                        f"{result['Carbohydrates (g)']} g"
                    )

                col4, col5, col6 = st.columns(3)

                with col4:
                    st.metric(
                        "Fat",
                        f"{result['Fats (g)']} g"
                    )

                with col5:
                    st.metric(
                        "Fibre",
                        f"{result['Fibre (g)']} g"
                    )

                with col6:
                    st.metric(
                        "Free Sugar",
                        f"{result['Free Sugar (g)']} g"
                    )

                st.subheader("🧪 Micronutrients")

                col7, col8, col9, col10 = st.columns(4)

                with col7:
                    st.metric(
                        "Sodium",
                        f"{result['Sodium (mg)']} mg"
                    )

                with col8:
                    st.metric(
                        "Calcium",
                        f"{result['Calcium (mg)']} mg"
                    )

                with col9:
                    st.metric(
                        "Iron",
                        f"{result['Iron (mg)']} mg"
                    )

                with col10:
                    st.metric(
                        "Vitamin C",
                        f"{result['Vitamin C (mg)']} mg"
                    )

                st.metric(
                    "Folate",
                    f"{result['Folate (µg)']} µg"
                )

                st.caption(
                    "Nutrition values are retrieved from the NutriSnap "
                    "nutrition dataset."
                )

# History Page
elif page == "History":
    st.title("📊 Meal History")
    st.info(
        "Your analyzed meals will appear here."
    )