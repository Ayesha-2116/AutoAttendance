import streamlit as st
from pymongo import MongoClient
from Dashboard import dashboard
from Register import userRegistration
# Define your custom CSS

custom_css = """
<style>
    .appview-container { /* background*/
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        margin-top: 50px
    }
    [data-testid="stAppViewBlockContainer"] {
        border: 2px solid #9e9e9e;  /* gray border color */
        padding: 20px;              /* Padding inside the section */
        border-radius: 10px;        /* Rounded corners */
        margin-bottom: 20px;        /* Space below the section */
        margin-top: 90px;           /* Set your desired height */
        width: 100%;                /* Set the width as needed */
    }


    #autoattend-tracker {
        margin-top: -70px;
        margin-left: 150px;
        color: DodgerBlue;
        /*background-color: DodgerBlue;
        width: 250%; */
    }

    [data-testid="stVerticalBlock"] {  /* login block*/
        margin-top: -270px
    } 
    
</style>
"""

# Inject the custom CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)
# Create a section with custom CSS classes
st.markdown('<div class="appview-container">', unsafe_allow_html=True)
st.markdown('<div class="stHeadingContainer">', unsafe_allow_html=True)
st.markdown('<h1 id="autoattend-tracker">', unsafe_allow_html=True)
st.markdown('<div data-testid="stVerticalBlock">', unsafe_allow_html=True)
st.markdown('<div data-testid="stVerticalBlockBorderWrapper" data-test-scroll-behavior="normal">', unsafe_allow_html=True)

# Connect to MongoDB
def get_mongo_client():
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
    return client
# Write the search function here:

def main():
    # Apply custom CSS style
    st.markdown("""
        <style>
            /* Define your CSS rules here */
            body {
                background-color: LightGray;
            }
            .stTextInput > div > div > input[type="text"],
            .stTextInput > div > div > input[type="password"] {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                width: 100%;
            }
            
            .stTextInput > div > div > input[type="text"]:hover,
            .stTextInput > div > div > input[type="password"]:hover {
                outline: DodgerBlue;
            }
            .stButton button {
                background-color: DodgerBlue;
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
                transition: background-color 0.3s, color 0.3s;
            }
        
            .stButton button:hover {
                background-color: #1e90ff; /* Slightly lighter DodgerBlue for hover effect */
                color: white;
            }
            .stButton button:active {
                background-color: #104e8b; /* Darker blue for active (click) effect */
                color: white;
            }
            .stButton button:focus {
                outline: none; /* Remove outline when button is focused */
                color: white;
                box-shadow: 0 0 0 2px rgba(30, 144, 255, 0.5); /* Add custom focus shadow */
            }
            .stButton button:hover,
            .stButton button:active,
            .stButton button:focus,
            .stButton button:visited {
                color: white; /* Ensure text color remains white in all states */
            }
        </style>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()