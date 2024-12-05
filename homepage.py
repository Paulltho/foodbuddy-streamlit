import streamlit as st

# Access the variable from st.secrets
SERVICE_URL = st.secrets["general"]["SERVICE_URL"]

def homepage():
    st.title("🍴 Welcome to FoodBuddy!")
    st.image("HealthyMeal.jpg", caption="")
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

st.markdown(
    """
    <style>
    div.stButton.red-button > button {
        font-size: 20px;
        font-weight: bold;
        padding: 10px 20px;
        margin-top: 10px;
        background-color: #FF5733;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    div.stButton.red-button > button:hover {
        background-color: #E74C3C;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
