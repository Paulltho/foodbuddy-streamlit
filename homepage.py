import streamlit as st

# Access the variable from st.secrets
SERVICE_URL = st.secrets["general"]["SERVICE_URL"]

def homepage():
    st.title("🍴 Welcome to FoodBuddy!")
    st.image("HealthyMeal.jpg", caption="Healthy Meal!")
    st.markdown(
        """
        FoodBuddy™ helps you analyze your meal and provides nutritional insights.
        Click **Next** to get started.
        """
    )
    # Navigate to the nutrition form when the "Next" button is clicked
    def go_to_nutrition_form():
        st.session_state["page"] = "nutrition_form"

    st.button("Next", on_click=go_to_nutrition_form)
