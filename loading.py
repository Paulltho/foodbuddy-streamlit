import streamlit as st

# Function to display the loading page
def loading():
    st.markdown(
        """
        <style>
        .centered-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .logo {
            width: 150px;
            height: auto;
        }
        .title {
            font-size: 2.5em;
            color: #333;
            margin-top: 20px;
        }
        </style>
        <div class="centered-container">
            <img class="logo" src="logo.png" alt="Logo">
            <div class="title">FoodBuddy™</div>
        </div>
        """,
        unsafe_allow_html=True
    )
