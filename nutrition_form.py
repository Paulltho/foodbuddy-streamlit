import streamlit as st
import requests
import pandas as pd

# Access the variable from st.secrets
SERVICE_URL = st.secrets["general"]["SERVICE_URL"]

def nutrition_form():

    # Add a "Go Back" button to navigate to the previous page
    def go_back():
        st.session_state["page"] = "homepage"
    st.button("Go Back", on_click=go_back)


    st.title("Calculate Your Daily Needs")
    st.markdown("Fill in your details below:")

    # Collect user inputs
    age = st.number_input("Age (years)", min_value=1, max_value=120, step=1)
    gender = st.radio("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", min_value=1, max_value=200, step=1)
    height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)

    st.subheader("Activity Level")
    activity_level = st.selectbox(
        "Choose your activity level",
        [
            "Sedentary (little or no exercise)",
            "Lightly active (light exercise/sports 1-3 days/week)",
            "Moderately active (moderate exercise/sports 3-5 days/week)",
            "Very active (hard exercise/sports 6-7 days a week)",
            "Super active (very hard exercise/physical job)",
        ],
    )

    # Streamlit Interface
    if st.button("Calculate your daily needs!"):
        user_inputs = {
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "activity_level": activity_level,
        }
        with st.spinner("Calculating..."):
            try:
                # Ensure the file content is sent to the API
                api_url = f"{SERVICE_URL}/calculate-daily-needs"
                response = requests.post(api_url, json=user_inputs)
                if response.status_code == 200:
                    result = response.json()
                else:
                    st.error(f"Failed to fetch daily needs. Status code: {response.status_code}")
                    return

                if result:
                    bmr = result["bmr"]
                    daily_caloric_needs = result["daily_caloric_needs"]
                    df = pd.DataFrame(result["nutrients"])
                    nutrients = result.get("nutrients", [])

                    st.subheader("Your Daily Nutritional Intake")
                    st.write(f"**Base Metabolic Rate (BMR):** {bmr} kcal/day")
                    for nutrient in nutrients:
                        st.markdown(
                            f"""
                            <div style="padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                                <h4 style="margin: 0;">{nutrient['Nutrient']}</h4>
                                <p style="margin: 5px 0;"><b>Daily Intake:</b> {nutrient['Your Daily Intake']}</p>
                                <p style="margin: 0; color: #555;">{nutrient['Description']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                     # Store the result in session state for navigation
                    st.session_state["df"] = df
                    st.session_state["daily_needs_ok"] = True




            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Display "Scan my plate" button if daily needs are calculated
    if st.session_state.get("daily_needs_ok", False):
        def go_to_scan():
            st.session_state["page"] = "meal_analysis"
        # st.button("Scan my plate!", on_click=go_to_scan)
        # Add a blank line before the button
        st.markdown("<br>", unsafe_allow_html=True)

        # Add a larger button with custom CSS styling
        st.markdown(
            """
            <style>
            .big-button {
                display: inline-block;
                font-size: 20px;
                font-weight: bold;
                padding: 10px 20px;
                margin-top: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                text-align: center;
            }
            .big-button:hover {
                background-color: #45a049;
            }
            </style>
            <div style="text-align: center;">
                <button class="big-button" onclick="window.location.href='/scan'">Scan my plate!</button>
            </div>
            """,
            unsafe_allow_html=True,
        )
