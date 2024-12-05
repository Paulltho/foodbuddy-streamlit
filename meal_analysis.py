import streamlit as st
import requests
import pandas as pd
import random
import time

# Access the variable from st.secrets
SERVICE_URL = st.secrets["general"]["SERVICE_URL"]


def relaunch_photo_analysis():
    st.session_state["page"] = "meal_analysis"


def remaining_nutrients_manual(df, detected_recipe_df):
    """
    Manually aligns and matches nutrient columns between the user's daily intake
    and detected recipe content. Calculates the remaining daily intake.

    Args:
        df (pd.DataFrame): User's daily intake with columns ["Nutrient", "Your Daily Intake"].
        detected_recipe_df (pd.DataFrame): Detected recipe content with columns ["Nutrient", "Quantity in your plate"].

    Returns:
        pd.DataFrame: A DataFrame showing remaining daily intake, original intake, and detected values.
    """

    # Manual mapping of nutrient names between the two DataFrames
    nutrient_mapping = {
        "Carbohydrates": "🍞 Carbohydrates (g)",
        "Proteins": "🥩 Proteins (g)",
        "Fats": "🥑 Fats (g)",
        "Calcium": "🥛 Calcium (mg)",
        "Iron": "🥬 Iron (mg)",
        "Magnesium": "🐟 Magnesium (mg)",
        "Sodium": "🧂 Sodium (mg)",
        "Vitamin C": "🍊 Vitamin C (mg)",
        "Vitamin D": "🌞 Vitamin D (µg)",
        "Vitamin A": "🥕 Vitamin A (µg)",
    }

    # Extract numeric values from "Your Daily Intake" and create "Daily Intake (Value)"
    if "Daily Intake (Value)" not in df.columns:
        df["Daily Intake (Value)"] = df["Your Daily Intake"].str.extract(r"([\d\.]+)").astype(float)

    # Align and match the rows manually
    aligned_daily_intake = df.set_index("Nutrient").rename(index=nutrient_mapping)
    aligned_detected_recipe = detected_recipe_df.set_index("Nutrient")

    # Ensure the detected recipe contains numeric values
    aligned_detected_recipe["Quantity in your plate"] = aligned_detected_recipe["Quantity in your plate"].astype(float)

    # Perform subtraction to calculate remaining nutrients
    remaining_nutrients = (
        aligned_daily_intake["Daily Intake (Value)"] - aligned_detected_recipe["Quantity in your plate"]
    )

    # Create the output DataFrame
    remaining_df = pd.DataFrame({
        "Nutrient": aligned_daily_intake.index,
        "Remaining Daily Intake": remaining_nutrients.values.round(0),
        "Original Daily Intake": aligned_daily_intake["Daily Intake (Value)"].values.round(0),
        "Detected Plate Content": aligned_detected_recipe["Quantity in your plate"].values.round(0),
    })

    # Reset index for clean display
    remaining_df.reset_index(drop=True, inplace=True)

    return remaining_df


def get_nutrients_and_KNN(recipe_name):
    # Fetch nutrients for the detected recipe
    nutrients_url = f"{SERVICE_URL}/tnutrients?recipe={recipe_name}"
    nutrients_response = requests.get(nutrients_url)

    if nutrients_response.status_code == 200:
        nutrients = nutrients_response.json().get("nutrients", [])
        if nutrients:
            detected_recipe_df = pd.DataFrame(nutrients)

            # Select only the relevant columns
            relevant_columns = [
                "Carbohydrates_(G)_total",
                "Protein_(G)_total",
                "Lipid_(G)_total",
                "Calcium_(MG)_total",
                "Iron_(MG)_total",
                "Magnesium_(MG)_total",
                "Sodium_(MG)_total",
                "Vitamin_C_(MG)_total",
                "Vitamin_D_(UG)_total",
                "Vitamin_A_(UG)_total",
            ]
            detected_recipe_df = detected_recipe_df[relevant_columns]

            # Manually rename columns to match emojis and friendly names
            column_rename_mapping = {
                "Carbohydrates_(G)_total": "🍞 Carbohydrates (g)",
                "Protein_(G)_total": "🥩 Proteins (g)",
                "Lipid_(G)_total": "🥑 Fats (g)",
                "Calcium_(MG)_total": "🥛 Calcium (mg)",
                "Iron_(MG)_total": "🥬 Iron (mg)",
                "Magnesium_(MG)_total": "🐟 Magnesium (mg)",
                "Sodium_(MG)_total": "🧂 Sodium (mg)",
                "Vitamin_C_(MG)_total": "🍊 Vitamin C (mg)",
                "Vitamin_D_(UG)_total": "🌞 Vitamin D (µg)",
                "Vitamin_A_(UG)_total": "🥕 Vitamin A (µg)",
            }
            detected_recipe_df.rename(columns=column_rename_mapping, inplace=True)

            # Reorder the columns to match the specified order
            ordered_columns = [
                "🍞 Carbohydrates (g)",
                "🥩 Proteins (g)",
                "🥑 Fats (g)",
                "🥛 Calcium (mg)",
                "🥬 Iron (mg)",
                "🐟 Magnesium (mg)",
                "🧂 Sodium (mg)",
                "🍊 Vitamin C (mg)",
                "🌞 Vitamin D (µg)",
                "🥕 Vitamin A (µg)",
            ]
            detected_recipe_df = detected_recipe_df[ordered_columns]

            # Round the values for a cleaner display
            detected_recipe_df = detected_recipe_df.round(0)

            # Reset the index for a clean table and display with headers
            nutrient_df = detected_recipe_df.transpose().reset_index()
            nutrient_df.columns = ["Nutrient", "Quantity in your plate"]
            nutrient_df["Quantity in your plate"] = nutrient_df["Quantity in your plate"].astype(int)

            nutrient_df_display = nutrient_df.copy().reset_index(drop=True)
            nutrient_df_display = nutrient_df_display.set_index("Nutrient")

            st.subheader("Nutritional Content of your plate")
            st.table(nutrient_df_display)
        else:
            st.error("No nutrient data found for this recipe.")

        remaining_df = remaining_nutrients_manual(st.session_state.get("df"),nutrient_df)

        # Automatically call KNN after plate analysis
        nutrient_values = remaining_df["Remaining Daily Intake"].tolist()
        if nutrient_values is not None:
            # Prepare payload for KNN
            payload = {
                "nutrient_values": nutrient_values,
            }

            # Call KNN API
            knn_url = f"{SERVICE_URL}/knn-recipes"
            knn_response = requests.post(knn_url, json=payload)

            if knn_response.status_code == 200:
                knn_results = knn_response.json()
                st.subheader("Recommended Recipes")
                # for recipe in knn_results.get("recipes", []):
                #     st.markdown(f"- **{recipe['recipe']}**")

                if "recipes" in knn_results:
                    recipes = knn_results["recipes"]
                    recipe_names = [f"**{recipe['recipe']}**" for recipe in recipes]

                    # Display recipes as a bulleted list
                    for recipe in recipe_names:
                        st.markdown(f"- {recipe}")
                else:
                    st.info("No recommendations found.")

            else:
                st.error(f"KNN API call failed with status code {knn_response.status_code}")
        else:
            st.error("User's daily nutrient data not found.")








def meal_analysis():

    # Add a "Go Back" button to navigate to the previous page
    def go_back():
        st.session_state["page"] = "nutrition_form"
    st.button("Go Back", on_click=go_back)

    st.title("Analyze Your Meal")
    st.markdown("Upload an image of your meal to analyze its nutritional content.")

    # Upload Section
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        if st.button("Analyze Plate Content"):
            with st.spinner("Analyzing your image..."):
                time.sleep(random.uniform(1, 3))  # Simulate processing delay

                try:
                    # Send the file to the API for plate analysis
                    files = {"file": uploaded_file.getvalue()}
                    api_url = f"{SERVICE_URL}/analyze-image"
                    response = requests.post(api_url, files=files)

                    if response.status_code == 200:
                        result = response.json()

                        if "error" in result:
                            st.error(f"Error: {result['error']}")
                        else:
                            confidence = result["probability"]
                            recipe_name = result["predicted_recipe_name"]


                            if confidence > 0.8:
                                st.success(f"We detected **{recipe_name}** on your plate with high confidence!")
                                get_nutrients_and_KNN(recipe_name)


                            elif 0.6 <= confidence <= 0.8:
                                st.warning(f"Your meal might be **{recipe_name}**. The model has moderate confidence.")
                                st.button("Yes, that's correct!", on_click=lambda : get_nutrients_and_KNN(recipe_name))
                                st.button("No, that's not correct.", on_click=relaunch_photo_analysis)

                            elif confidence < 0.6:
                                st.warning("The model is unsure about your meal. Could you help us improve?")
                                user_input = st.text_input("What is on your plate?")
                                st.button("Submit", on_click=relaunch_photo_analysis)

                    else:
                        st.error(f"API call failed with status code {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
