import streamlit as st
import time
from loading import loading
from homepage import homepage
from nutrition_form import nutrition_form
from meal_analysis import meal_analysis

def go_to_homepage():
    st.session_state["page"] = "homepage"

# Set up session state test
if "page" not in st.session_state:
    st.session_state["page"] = "loading"

# Navigation logic
if st.session_state["page"] == "loading":
    loading()
    time.sleep(2)
    go_to_homepage()
if st.session_state["page"] == "homepage":
    homepage()
elif st.session_state["page"] == "nutrition_form":
    nutrition_form()
elif st.session_state["page"] == "meal_analysis":
    meal_analysis()
