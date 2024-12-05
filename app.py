import streamlit as st
from homepage import homepage
from nutrition_form import nutrition_form
from meal_analysis import meal_analysis

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
