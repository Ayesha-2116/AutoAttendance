import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB connection details
URI = "mongodb+srv://AutoAttendNew:AutoAttendNew@cluster0.vlu3rze.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = 'attendance_system'

def connect_to_mongodb(uri):
    """
    Establishes a connection to MongoDB and returns the database and required collections.
    """
    client = MongoClient(uri)
    db = client[DB_NAME]
    return db, db['attendance'], db['workshops'], db['students']

# Define your custom CSS
custom_css = """
<style>
    .appview-container { /* background */
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        margin-top: 50px;
    }
    [data-testid="stAppViewBlockContainer"] {
        border: 2px solid #9e9e9e;  /* gray border color */
        padding: 20px;              /* Padding inside the section */
        border-radius: 10px;        /* Rounded corners */
        margin-bottom: 20px;        /* Space below the section */
        margin-top: 90px;           /* Set your desired height */
        width: 100%;                /* Set the width as needed */
    }
</style>
"""

# Inject the custom CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)

def student_search():
    st.title("Student Workshop Attendance Search")
    search_term = st.text_input("Enter Student ID", placeholder="Search for a student")
    search_button = st.button("Search")

    if search_button:
        # Connect to MongoDB
        db, attendance_collection, workshops_collection, students_collection = connect_to_mongodb(URI)

        # Query students collection for student name
        student = students_collection.find_one({"studentID": search_term})

        if not student:
            st.error(f"Student ID '{search_term}' not found.")
        else:
            student_name = f"{student['firstName']} {student['lastName']}"

            # Query attendance collection
            attendance_records = list(attendance_collection.find({"username": search_term}))

            if not attendance_records:
                st.write(f"No attendance records found for student ID '{search_term}'.")
            else:
                workshop_ids = [record['workshopId'] for record in attendance_records]
                workshop_counts = {workshop_id: workshop_ids.count(workshop_id) for workshop_id in workshop_ids}

                # Query workshops collection
                workshops = workshops_collection.find({"workshopId": {"$in": workshop_ids}})
                workshops_dict = {workshop['workshopId']: workshop for workshop in workshops}

                # Calculate total count of workshops attended
                total_workshops_attended = sum(workshop_counts.values())

# Prepare data for display
                data = []
                for record in attendance_records:
                    workshop = workshops_dict.get(record['workshopId'], {})
                    data.append({
                        "Student ID": record['username'],
                        "Student Name": student_name,
                        "Workshop Name": workshop.get('workshopName', 'Unknown'),
                        "Date & Time": workshop.get('date', 'Unknown'),
                        "Count": workshop_counts[record['workshopId']]
                    })

                # Convert data to DataFrame
                df = pd.DataFrame(data)

                # Fill NaN values with empty strings or other appropriate placeholders
                df = df.fillna('')

                # Add total count row
                df.loc['Total'] = pd.Series({
                    'Student ID': '',
                    'Student Name': '',
                    'Workshop Name': '',
                    'Date & Time': '',
                    'Count': total_workshops_attended
                })

                # Display the DataFrame as a table
                st.table(df)


def main():
    # Apply custom CSS style
    st.markdown("""
        <style>
            /* Define your CSS rules here */
            body {
                background-color: LightGray;
            }
            .stTextInput > div > div > input[type="text"] {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                width: 100%;
            }
            .stTextInput > div > div > input[type="text"]:hover {
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
    
    # Display the student search functionality
    student_search()

if __name__ == "__main__":
    main()
