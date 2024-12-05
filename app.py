import streamlit as st
from homepage import homepage
from nutrition_form import nutrition_form
from meal_analysis import meal_analysis

# Custom CSS for "Poppins" and button styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    div.stButton {
        display: flex;
        justify-content: center; /* Centers the button horizontally */
        margin-top: 15px; /* Adds spacing above the button */
    }
    div.stButton > button {
        font-size: 20px; /* Large font for buttons */
        font-weight: bold; /* Makes button text bold */
        padding: 12px 24px; /* Generous padding for a bigger button */
        background-color: #FF5733; /* Vibrant red background */
        color: white; /* White text for contrast */
        border: none; /* Removes default button border */
        border-radius: 10px; /* Rounded corners for buttons */
        cursor: pointer; /* Pointer cursor on hover */
    }
    div.stButton > button:hover {
        background-color: #E74C3C; /* Darker red for hover effect */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Set up session state test
if "page" not in st.session_state:
    st.session_state["page"] = "homepage"

# Navigation logic
if st.session_state["page"] == "homepage":
    homepage()
elif st.session_state["page"] == "nutrition_form":
    nutrition_form()
elif st.session_state["page"] == "meal_analysis":
    meal_analysis()
