import time
import streamlit as st
import cv2
import numpy as np
import base64
from pymongo import MongoClient
from io import BytesIO
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
        
        .appview-container { /* background*/
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        margin-top: 50px
        }

        [data-testid="stSidebar"] {
            background-color: #DCDCDC;  
        }
            
        [playsinline] {
            border-left: 2px solid DodgerBlue; /* Left border */
            border-right: 2px solid DodgerBlue; /* Right border */
            padding: 1px;              /* Padding inside the section */
            border-radius: 10px;        /* Rounded corners */
            margin-bottom: 20px;        /* Space below the section */
            margin-top: 10px;           /* Set your desired height */
            width: 100%;                /* Set the width as needed */
        }
        
        [data-testid="stCameraInputButton"] { /* this is text below camera*/
            content: 'Capture Photo';
            font-weight: 400;
            background-color: DodgerBlue;
            color: white;
            height: 45px;
            border-radius: 6px;
        }
            
        [data-testid="stVerticalBlock"] {  /* login block*/
            margin-top: -100px
    }
    </style>
""", unsafe_allow_html=True) 



# Connect to MongoDB (Make sure your MongoDB server is running)
client = MongoClient('mongodb://localhost:27017/')
db = client['Attendence']
collection = db['students']

# Streamlit interface
st.title('Register Student Records')

# Input fields for student name and ID
# Input fields for student name and ID
placeholder_student_name = st.empty()
placeholder_student_id = st.empty()
placeholder_camera = st.empty()
student_name = placeholder_student_name.text_input('Enter Student Name:',  key='student_name_input1')
student_id = placeholder_student_id.text_input('Enter Student ID:', key='student_id_input1')


def save_to_mongodb(name, student_id, image):
    # Check if student ID already exists
    existing_student = collection.find_one({'student_id': student_id})
    
    if existing_student:
        st.warning(f"Student with ID '{student_id}' already exists. Please use a different student ID.")
        return
    # Convert image to bytes for storage
    _, buffer = cv2.imencode('.jpg', image)
    image_bytes = BytesIO(buffer).getvalue()
    
    # Convert bytes to base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    # Prepare document to insert into MongoDB
    document = {
        'name': name,
        'student_id': student_id,
        'photo': image_base64
    }

    # Insert document into MongoDB collection
    collection.insert_one(document)
    st.success('Data saved successfully!')
    #code to refresh fields
    student_name = placeholder_student_name.text_input('Enter Student Name:',  key='student_name_input2')
    student_id = placeholder_student_id.text_input('Enter Student ID:', key='student_id_input2')
    img_file_buffer = placeholder_camera.camera_input("Capture Photo", key='2')
   

# Camera input
img_file_buffer = placeholder_camera.camera_input("Capture Photo", key='1')

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Display the captured image
    #st.image(cv2_img, channels="BGR")

# Save button to save data to MongoDB
if st.button('Save Data'):
    if student_name.strip() != '' and student_id.strip() != '' and img_file_buffer is not None:
        save_to_mongodb(student_name, student_id, cv2_img)
    else:
        st.warning('Please enter student name, student ID, and capture a photo before saving.')