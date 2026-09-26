import streamlit as st
from database.db import initialize_database, save_profile
from services.calorie_service import(
    calculate_bmr,
    calculate_tdee,
    calculate_calorie_target,
    calculate_macros
)

# Page configuration
st.set_page_config(
    page_title = "NutriSnap",
    page_icon = "🥗"
)
initialize_database()

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
            value=21,
            step=1
        )
        sex = st.selectbox(
            "Sex",
            ["Male", "Female"]
        )
        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=250.0,
            value=170.0,
            step=1.0
        )

    with col2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=300.0,
            value=70.0,
            step=0.5
        )
        activity_level = st.selectbox(
            "Activity Level",
            [
                "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active",
                "Extra Active"
            ]
        )
        goal = st.selectbox(
            "Goal",
            [
                "Lose Weight",
                "Maintain Weight",
                "Gain Weight"
            ]
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
    st.title("📸 Meal Analysis")
    st.info(
        "AI-powered food recognition will be added here."
    )

# History Page
elif page == "History":
    st.title("📊 Meal History")
    st.info(
        "Your analyzed meals will appear here."
    )