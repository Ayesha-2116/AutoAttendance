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

# Streamlit app
def main():
    st.title("Attendance Upload")

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

if __name__ == "__main__":
    main()
