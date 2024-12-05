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
    div.stButton {
        display: flex;
        justify-content: center; /* Centers the button horizontally */
        margin-top: 10px; /* Adds spacing above the button */
    }
    div.stButton > button {
        font-size: 20px; /* Makes the button text larger */
        font-weight: bold; /* Makes the button text bold */
        padding: 10px 20px; /* Adds padding around the text */
        background-color: #FF5733; /* Sets the button background color to red */
        color: white; /* Sets the text color to white */
        border: none; /* Removes the button border */
        border-radius: 8px; /* Adds rounded corners */
        cursor: pointer; /* Changes the cursor to a pointer on hover */
    }
    div.stButton > button:hover {
        background-color: #E74C3C; /* Darkens the red color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)
