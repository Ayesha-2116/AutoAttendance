import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import threading
import streamlit as st
from pymongo import MongoClient
from collections import defaultdict

URI = "mongodb+srv://AutoAttendNew:AutoAttendNew@cluster0.vlu3rze.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = 'attendance_system'

def connect_to_mongodb(uri):
    client = MongoClient(uri)
    db = client[DB_NAME]

    students_collection = db['students']
    attendance_collection = db['attendance']

    # Retrieve studentID, firstName, and lastName
    students = students_collection.find({}, {'studentID': 1, 'firstName': 1, 'lastName': 1, 'email': 1})
    attendance_count = defaultdict(lambda: {'count': 0, 'email': ''})

    for student in students:
        student_id = student['studentID']
        student_name = f"{student['firstName']} {student['lastName']}"

        count = attendance_collection.count_documents({'username': student_id})
        attendance_count[student_name] = {'count': count, 'email': student['email']}

    attendance_count = dict(attendance_count)
    return attendance_count


def send_email(subject, body, to_email, from_email, password):
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(message)
        server.quit()
        print(f"Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

def job():
    from_email = "bivektest97@gmail.com"
    password = "ypxt tsbh okvx qali"

    attendance_count = connect_to_mongodb(URI)
    # attendance_count = {'Bivek Kasaju': {'count': 3, 'email': 'trollboi7777@gmail.com'}, 'Test Kasaju': {'count': 0, 'email': '18bivek@gmail.com'}}

    for student_name, info in attendance_count.items():
        subject = "Workshop Count"
        count = info['count']
        body = f"Hello {student_name},\n\nYour current workshop count is {count}.\n\nBest regards,\nAutoAttend Team"
        to_email = info['email']

        send_email(subject, body, to_email, from_email, password)


def schedule_task():
    if user_selected_day == "Monday":
        schedule.every().monday.at(f"{task_hour:02}:{task_minute:02}").do(job)
    elif user_selected_day == "Tuesday":
        schedule.every().tuesday.at(f"{task_hour:02}:{task_minute:02}").do(job)
    elif user_selected_day == "Wednesday":
        schedule.every().wednesday.at(f"{task_hour:02}:{task_minute:02}").do(job)
    elif user_selected_day == "Thursday":
        schedule.every().thursday.at(f"{task_hour:02}:{task_minute:02}").do(job)
    elif user_selected_day == "Friday":
        schedule.every().friday.at(f"{task_hour:02}:{task_minute:02}").do(job)
    elif user_selected_day == "Saturday":
        schedule.every().saturday.at(f"{task_hour:02}:{task_minute:02}").do(job)
    elif user_selected_day == "Sunday":
        schedule.every().sunday.at(f"{task_hour:02}:{task_minute:02}").do(job)

def run_scheduler():
    schedule_task()
    # schedule.every().saturday.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

st.title("Schedule Email (Weekly)")

user_selected_day = st.selectbox("Day:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
task_hour = st.number_input("Hour:", min_value=0, max_value=23, value=9)
task_minute = st.number_input("Minute:", min_value=0, max_value=59, value=0)

st.write(f"Selected day: {user_selected_day}")
st.write(f"Selected time: {task_hour:02d}:{task_minute:02d}")



if st.button("Schedule"):
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    st.success("Schedule has been triggered!")



st.title("Email now")
if st.button("Send Email"):
    job()
    st.success("Email sent!")




