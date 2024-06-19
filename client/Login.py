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

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'registered' not in st.session_state:
    st.session_state.registered = False

def login():
    st.title("AutoAttend Tracker")
    st.header('Login')
    email = st.text_input('Email Address', placeholder='Enter email.', )
    password = st.text_input('Password', type='password', placeholder='Enter password.')
    loginButton = st.button('Login')
     # Validate login credentials
    if loginButton:
        if email.strip() == '' or password.strip() == '':
            st.error('Please fill in all required fields.')
        else:
            client = get_mongo_client()
            db = client['Attendence']  # Replace with your database name
            users_collection = db['Users']  # Replace with your collection name
            
            # Perform login authentication here
            user = users_collection.find_one({'email': email})
            if user:
                #st.write("User found:", user)  # Debugging statement
                if user['password'] == password:
                    st.session_state['logged_in'] = True
                    st.success('Login successful!')
                    
                else:
                    st.error('Invalid password. Please try again.')
            else:
                st.error('User not found. Please try again.')
    st.write("Don't have an account? Register [here](?page=register)")


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
    
     # Check for URL parameter
    query_params = st.query_params
    if 'page' in query_params and query_params['page'] == 'register':
        st.session_state['registered'] = True
    else:
        st.session_state['registered'] = False

    if st.session_state['registered']:
        userRegistration()  # Call the registration function
    elif st.session_state['logged_in']:
        dashboard()
    else:
        # Call the login function
        login()
   


if __name__ == "__main__":
    main()