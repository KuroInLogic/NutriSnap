import streamlit as st
from PIL import Image
from database.db import initialize_database, save_profile, get_profile
from services.calorie_service import(
    calculate_bmr,
    calculate_tdee,
    calculate_calorie_target,
    calculate_macros
)
from services.nutrition_service import (
    load_nutrition_data,
    find_food,
    search_foods,
    calculate_portion_nutrition,
    compare_with_daily_targets
)
from services.ai_service import analyze_food_image

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
        "Upload a photo of your meal to begin nutrition analysis."
    )
    st.subheader("📸 Upload Meal Image")
    uploaded_image = st.file_uploader(
        "Choose a meal image",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_image is not None:
        image = Image.open(uploaded_image)

        st.image(
            image,
            caption="Uploaded Meal",
            width="stretch"
        )

        if st.button("🔍 Identify Food"):

            with st.spinner("Analyzing your meal..."):
                try:
                    image_bytes = uploaded_image.getvalue()
                    image_type = uploaded_image.type

                    ai_result = analyze_food_image(
                        image_bytes,
                        image_type
                        )

                    st.success("Food identified!")

                    st.subheader("🤖 AI Food Recognition")

                    lines = ai_result.splitlines()

                    food_name_ai = ""
                    confidence = ""

                    for line in lines:
                        if line.lower().startswith("food:"):
                            food_name_ai = line.split(":", 1)[1].strip()

                        elif line.lower().startswith("confidence:"):
                            confidence = line.split(":", 1)[1].strip()

                    if food_name_ai:

                        st.write(
                            f"**Detected Food:** {food_name_ai}"
                        )

                        if confidence:
                            st.write(
                                f"**AI Confidence:** {confidence}"
                            )

                        matches = search_foods(
                            food_name_ai,
                            limit=15
                            )

                        if matches:
                            st.subheader(
                                    "🔎 Possible Nutrition Database Matches"
                            )
                            st.session_state["food_matches"] = matches

                        else:
                            st.warning(
                                "No matching food was found "
                                "in the NutriSnap nutrition database."
                            )

                except Exception as e:
                    st.error(
                        f"Unable to analyze the image: {e}"
                    )

        # Food Selection
        if "food_matches" in st.session_state:
            matches = st.session_state["food_matches"]
            # Best match suggested by the ranking system
            suggested_food = matches[0]

            st.subheader("Nutrition Database Match")
            st.write(
                f"**Suggested Food:** {suggested_food['Dish Name']}"
            )

            # Use the best match by default
            st.session_state["selected_food"] = suggested_food

            # Allow the user to correct the suggestion if needed
            if len(matches) > 1:
                with st.expander("🔄 Not the correct food? Choose another"):

                    match_names = [
                        match["Dish Name"]
                        for match in matches
                    ]

                    selected_food_name = st.selectbox(
                        "Select the correct food:",
                        match_names,
                        key="alternative_food"
                    )

                    selected_match = next(
                        match for match in matches
                        if match["Dish Name"] == selected_food_name
                    )
                    st.session_state["selected_food"] = selected_match


    # Food Confirmation
    if "selected_food" in st.session_state:

        st.subheader("✅ Confirm Food")

        selected_food = st.session_state["selected_food"]

        st.write(
            f"**Selected:** {selected_food['Dish Name']}"
        )

        if st.button("✅ Confirm Food"):

            st.session_state["confirmed_food"] = selected_food

            st.success(
                f"Confirmed: {selected_food['Dish Name']}"
            )


    # Portion Size and Nutrition Calculation
    if "confirmed_food" in st.session_state:

        confirmed_food = st.session_state["confirmed_food"]

        st.divider()
        st.subheader("⚖️ Portion Size")

        portion_grams = st.number_input(
            "Enter portion size (grams)",
            min_value=1.0,
            value=100.0,
            step=10.0
        )

        if st.button("🧮 Calculate Nutrition"):
            nutrition = calculate_portion_nutrition(
                confirmed_food,
                portion_grams
            )
            
            profile = get_profile()
            if profile:
                calorie_target = profile[8]

                macro_targets = {
                    "protein": profile[9],
                    "carbs": profile[10],
                    "fat": profile[11]
                }

                comparison = compare_with_daily_targets(
                    nutrition,
                    calorie_target,
                    macro_targets
                )

                st.subheader("🎯 Your Daily Target Comparison")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Calories",
                        f"{comparison['Calories']}%",
                        "of daily target"
                    )

                with col2:
                    st.metric(
                        "Protein",
                        f"{comparison['Protein']}%",
                        "of daily target"
                    )

                with col3:
                    st.metric(
                        "Carbohydrates",
                        f"{comparison['Carbohydrates']}%",
                        "of daily target"
                    )

                with col4:
                    st.metric(
                        "Fat",
                        f"{comparison['Fat']}%",
                        "of daily target"
                    )

            else:
                st.info(
                    "Please calculate your daily nutrition requirements "
                    "in My Profile to see your personalized comparison."
                )

            st.subheader("🥗 Nutrition Information")
            st.write(
                f"**Food:** {confirmed_food['Dish Name']}"
            )
            st.write(
                f"**Portion:** {portion_grams:.0f} g"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Calories",
                    f"{nutrition['Calories']:.1f} kcal"
                )
                st.metric(
                    "Protein",
                    f"{nutrition['Protein']:.1f} g"
                )

            with col2:
                st.metric(
                    "Carbohydrates",
                    f"{nutrition['Carbohydrates']:.1f} g"
                )
                st.metric(
                    "Fat",
                    f"{nutrition['Fat']:.1f} g"
                )

            with col3:
                st.metric(
                    "Fibre",
                    f"{nutrition['Fibre']:.1f} g"
                )
                st.metric(
                    "Free Sugar",
                    f"{nutrition['Free Sugar']:.1f} g"
                )

# History Page
elif page == "History":
    st.title("📊 Meal History")
    st.info(
        "Your analyzed meals will appear here."
    )