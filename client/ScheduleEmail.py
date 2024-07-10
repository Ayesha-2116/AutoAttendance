import streamlit as st

# Apply custom CSS style
st.markdown("""
    <style>
        body {
            background-color: LightGray;
        }
        .stRadio > div {
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 8px;
            width: 100%;
        }
        .stRadio > div > label {
            color: DodgerBlue;
        }
        .stRadio > div > div > label {
            background-color: white;
            color: black;
            padding: 8px;
            border-radius: 5px;
        }
        .stRadio > div > div > label:hover {
            background-color: DodgerBlue;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit interface
st.title('Schedule Email')

# Dropdown or radio button for scheduling options
options = ["Weekly", "Bi-weekly", "Monthly"]
schedule = st.radio("Select your email schedule:", options, index=0)

st.write(f"Selected option: {schedule}")
