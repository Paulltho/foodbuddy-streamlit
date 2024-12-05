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
        detected_recipe_df (pd.DataFrame): Detected recipe content with columns ["Nutrient", "Value"].

    Returns:
        pd.DataFrame: A DataFrame showing remaining daily intake, original intake, and detected values.
    """

    # Define manual column mapping
    nutrient_mapping = {
        "Carbohydrates": "Carbohydrates_(G)_total",
        "Proteins": "Protein_(G)_total",
        "Fats": "Lipid_(G)_total",
        "Calcium": "Calcium_(MG)_total",
        "Iron": "Iron_(MG)_total",
        "Magnesium": "Magnesium_(MG)_total",
        "Sodium": "Sodium_(MG)_total",
        "Vitamin C": "Vitamin_C_(MG)_total",
        "Vitamin D": "Vitamin_D_(UG)_total",
        "Vitamin A": "Vitamin_A_(UG)_total",
    }

    # Prepare daily intake values (strip units and convert to floats)
    df["Daily Intake (Value)"] = df["Your Daily Intake"].str.extract(r"([\d\.]+)").astype(float)

    # Align detected recipe values using the mapping
    detected_values = detected_recipe_df.loc[list(nutrient_mapping.values()), 0]

    # Perform subtraction to calculate remaining nutrients
    remaining_nutrients = df["Daily Intake (Value)"].values - detected_values.values

    # Create output DataFrame
    remaining_df = pd.DataFrame({
        "Nutrient": df["Nutrient"],
        "Remaining Daily Intake": remaining_nutrients,
        "Original Daily Intake": df["Daily Intake (Value)"].values,
        "Detected Plate Content": detected_values.values,
    })

    return remaining_df


def get_nutrients_and_KNN(recipe_name):
    # Nutrient-to-emoji mapping
    nutrient_emojis = {
        "Carbohydrates": "🍞",
        "Proteins": "🥩",
        "Fats": "🥑",
        "Calcium": "🥛",
        "Iron": "🥬",
        "Magnesium": "🐟",
        "Sodium": "🧂",
        "Vitamin C": "🍊",
        "Vitamin D": "🌞",
        "Vitamin A": "🥕",
    }

    # Fetch nutrients for the detected recipe
    nutrients_url = f"{SERVICE_URL}/tnutrients?recipe={recipe_name}"
    nutrients_response = requests.get(nutrients_url)

    if nutrients_response.status_code == 200:
        nutrients = nutrients_response.json().get("nutrients", [])
        if nutrients:
            detected_recipe_df = pd.DataFrame(nutrients)

            # Select only columns ending with "_total"
            relevant_columns = [col for col in detected_recipe_df.columns if "_total" in col]
            detected_recipe_df = detected_recipe_df[relevant_columns].transpose()

            # Rename the index for user-friendliness and add emojis
            def map_nutrient_name(name):
                # Extract base nutrient name
                base_name = name.split("_")[0].replace("Vitamin", "Vitamin ").replace("_", " ")
                emoji = nutrient_emojis.get(base_name.strip(), "🍽️")  # Default emoji
                # Replace units and append emoji
                friendly_name = (
                    name.replace("_(G)_total", " (g)")
                    .replace("_(MG)_total", " (mg)")
                    .replace("_(UG)_total", " (µg)")
                )
                return f"{emoji} {friendly_name.replace('_', ' ')}"

            detected_recipe_df.index = detected_recipe_df.index.map(map_nutrient_name)

            # Round nutrient values
            detected_recipe_df = detected_recipe_df.round(0)

            # Convert to a DataFrame for headers
            nutrient_df = detected_recipe_df.reset_index()
            nutrient_df.columns = ["Nutrient", "Quantity in your plate"]

            st.subheader("Nutritional Content of your plate")
            st.table(nutrient_df)
        else:
            st.error("No nutrient data found for this recipe.")

        remaining_df = remaining_nutrients_manual(st.session_state.get("df"),detected_recipe_df)

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
