# import streamlit as st
# import pandas as pd
# from pymongo import MongoClient
# from datetime import datetime, timedelta

# # MongoDB connection
# client = MongoClient("mongodb+srv://AutoAttendNew:AutoAttendNew@cluster0.vlu3rze.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client['attendance_system']

# # Function to insert attendance
# def insert_attendance(username, workshop_id, in_time, present):
#     attendance_record = {
#         "username": username,
#         "workshopId": workshop_id,
#         "inTime": in_time,
#         "present": present
#     }
#     db.attendance.insert_one(attendance_record)

# # Streamlit app
# def main():
#     st.title("Attendance Upload")

#     # File upload and validation
#     uploaded_file = st.file_uploader("Upload Excel file", type=["xls", "xlsx"])
#     if uploaded_file is not None:
#         try:
#             df = pd.read_excel(uploaded_file)

#             # Check if required columns are present
#             required_columns = ['Student_ID', 'Student Name', 'Workshop Name']
#             if not set(required_columns).issubset(df.columns):
#                 st.error("Excel file must contain columns: 'Student_ID', 'Student Name', 'Workshop Name'.")
#                 return

#             # Check if all rows have these columns filled
#             if df[required_columns].isnull().values.any():
#                 st.error("All rows must have 'Student_ID', 'Student Name', 'Workshop Name' filled.")
#                 return

#             # Check if all student IDs exist in the student table
#             student_ids = df['Student_ID'].tolist()
#             existing_students = db.students.find({'studentID': {'$in': student_ids}})
#             existing_student_ids = {student['studentID'] for student in existing_students}

#             missing_student_ids = [sid for sid in student_ids if sid not in existing_student_ids]
#             if missing_student_ids:
#                 st.error(f"Student IDs not found in database: {', '.join(map(str, missing_student_ids))}")
#                 return

#             # Insert attendance records
#             for index, row in df.iterrows():
#                 student_id = row['Student_ID']
#                 student_name = row['Student Name']
#                 workshop_name = row['Workshop Name']

#                 # Fetch workshop ID based on workshop_name
#                 workshop = db.workshops.find_one({'workshopName': workshop_name})
#                 if workshop:
#                     workshop_id = workshop['workshopId']
#                     in_time = workshop['date'] + timedelta(hours=7)  # Adjust as per timezone
#                     present = False  # Assuming default is not present

#                     # Fetch username from students table based on student_id
#                     student = db.students.find_one({'studentID': student_id})
#                     if student:
#                         username = student['username']
#                         insert_attendance(username, workshop_id, in_time, present)
#                         st.success(f"Attendance recorded for {student_name} at {workshop_name}.")
#                 else:
#                     st.warning(f"Workshop '{workshop_name}' not found in database.")

#         except Exception as e:
#             st.error(f"Error processing file: {e}")

# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection
client = MongoClient("mongodb+srv://AutoAttendNew:AutoAttendNew@cluster0.vlu3rze.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['attendance_system']

# Function to insert attendance
def insert_attendance(username, workshop_id, in_time, present):
    attendance_record = {
        "username": username,
        "workshopId": workshop_id,
        "inTime": in_time,
        "present": present
    }
    db.attendance.insert_one(attendance_record)

# Function to insert workshop
def insert_workshop(workshop_details, presenter_details):
    date = workshop_details['date']
    time = workshop_details['time']
    combined_datetime = datetime.combine(date, time)

    workshop_record = {
        "workshopId": workshop_details['workshopId'],
        "workshopName": workshop_details['workshopName'],
        "date": combined_datetime,
        "location": workshop_details['location'],
        "presenter": presenter_details,
        "wReview": workshop_details['wReview']
    }
    db.workshops.insert_one(workshop_record)
    st.success("Workshop added successfully.")

# Helper functions to get presenter details
def get_presenter_id_by_username(username):
    workshop = db.workshops.find_one({"presenter.username": username}, {"_id": 0, "presenter.presenterID": 1})
    return workshop['presenter']['presenterID'] if workshop and 'presenter' in workshop else None

def get_presenter_email_by_username(username):
    workshop = db.workshops.find_one({"presenter.username": username}, {"_id": 0, "presenter.email": 1})
    return workshop['presenter']['email'] if workshop and 'presenter' in workshop else None

def get_presenter_firstName_by_username(username):
    workshop = db.workshops.find_one({"presenter.username": username}, {"_id": 0, "presenter.firstName": 1})
    return workshop['presenter']['firstName'] if workshop and 'presenter' in workshop else None

def get_presenter_lastName_by_username(username):
    workshop = db.workshops.find_one({"presenter.username": username}, {"_id": 0, "presenter.lastName": 1})
    return workshop['presenter']['lastName'] if workshop and 'presenter' in workshop else None

def get_presenter_usernames():
    workshops = db.workshops.find({}, {"_id": 0, "presenter.username": 1})
    presenter_usernames = [workshop['presenter']['username'] for workshop in workshops]
    return presenter_usernames

# Streamlit app
def main():
    st.title("Workshop and Attendance Management")

    # Tabs for different sections
    tab1, tab2 = st.tabs(["Upload Attendance", "Add Workshop"])

    with tab1:
        st.header("Attendance Upload")
        
        # File upload and validation
        uploaded_file = st.file_uploader("Upload Excel file", type=["xls", "xlsx"])
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)

                # Check if required columns are present
                required_columns = ['Student_ID', 'Student Name', 'Workshop Name']
                if not set(required_columns).issubset(df.columns):
                    st.error("Excel file must contain columns: 'Student_ID', 'Student Name', 'Workshop Name'.")
                    return

                # Check if all rows have these columns filled
                if df[required_columns].isnull().values.any():
                    st.error("All rows must have 'Student_ID', 'Student Name', 'Workshop Name' filled.")
                    return

                # Check if all student IDs exist in the student table
                student_ids = df['Student_ID'].tolist()
                existing_students = db.students.find({'studentID': {'$in': student_ids}})
                existing_student_ids = {student['studentID'] for student in existing_students}

                missing_student_ids = [sid for sid in student_ids if sid not in existing_student_ids]
                if missing_student_ids:
                    st.error(f"Student IDs not found in database: {', '.join(map(str, missing_student_ids))}")
                    return

                # Insert attendance records
                for index, row in df.iterrows():
                    student_id = row['Student_ID']
                    student_name = row['Student Name']
                    workshop_name = row['Workshop Name']

                    # Fetch workshop ID based on workshop_name
                    workshop = db.workshops.find_one({'workshopName': workshop_name})
                    if workshop:
                        workshop_id = workshop['workshopId']
                        in_time = workshop['date'] + timedelta(hours=7)  # Adjust as per timezone
                        present = False  # Assuming default is not present

                        # Fetch username from students table based on student_id
                        student = db.students.find_one({'studentID': student_id})
                        if student:
                            username = student['username']
                            insert_attendance(username, workshop_id, in_time, present)
                            st.success(f"Attendance recorded for {student_name} at {workshop_name}.")
                    else:
                        st.warning(f"Workshop '{workshop_name}' not found in database.")

            except Exception as e:
                st.error(f"Error processing file: {e}")

    with tab2:
        st.header("Add Workshop and Presenter")

        presenter_names = get_presenter_usernames()
        selected_presenter = st.selectbox("Select Presenter", options=presenter_names + ["Add New Presenter"])

        if selected_presenter == "Add New Presenter" or st.session_state.get('add_presenter_mode', False):
            st.session_state.add_presenter_mode = True
            with st.form(key='add_presenter_form'):
                st.subheader("Add New Presenter")
                presenter_id = st.text_input("Presenter ID")
                username = st.text_input("Username")
                email = st.text_input("Email")
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                p_review = st.text_area("Presenter Review", "")
                workshop_id = st.text_input("Workshop ID")
                workshop_name = st.text_input("Workshop Name")
                date = st.date_input("Date", min_value=datetime.today())
                time = st.time_input("Time")
                location = st.text_input("Location")
                w_review = st.text_area("Workshop Review", "")
                submit_button = st.form_submit_button("Submit")

                if submit_button:
                    presenter_details = {
                        "presenterID": presenter_id,
                        "username": username,
                        "email": email,
                        "firstName": first_name,
                        "lastName": last_name,
                        "pReview": p_review
                    }
                    workshop_details = {
                        "workshopId": workshop_id,
                        "workshopName": workshop_name,
                        "date": date,
                        "time": time,
                        "location": location,
                        "wReview": w_review
                    }
                    insert_workshop(workshop_details, presenter_details)
                    st.session_state.add_presenter_mode = False

        if not st.session_state.get('add_presenter_mode', False):
            if selected_presenter != "Add New Presenter":
                presenter_id = get_presenter_id_by_username(selected_presenter)
                presenter_email = get_presenter_email_by_username(selected_presenter)
                presenter_fn = get_presenter_firstName_by_username(selected_presenter)
                presenter_ln = get_presenter_lastName_by_username(selected_presenter)
                presenter_details = {
                    "presenterID": presenter_id,
                    "username": selected_presenter,
                    "email": presenter_email,
                    "firstName": presenter_fn,
                    "lastName": presenter_ln
                }
                if presenter_id:
                    st.subheader("Enter Workshop Details")
                    workshop_id = st.text_input("Workshop ID")
                    workshop_name = st.text_input("Workshop Name")
                    date = st.date_input("Date", min_value=datetime.today())
                    time = st.time_input("Time")
                    location = st.text_input("Location")
                    w_review = st.text_area("Workshop Review", "")

                    if st.button("Add Workshop"):
                        workshop_details = {
                            "workshopId": workshop_id,
                            "workshopName": workshop_name,
                            "date": date,
                            "time": time,
                            "location": location,
                            "wReview": w_review
                        }
                        insert_workshop(workshop_details, presenter_details)

if __name__ == "__main__":
    main()
