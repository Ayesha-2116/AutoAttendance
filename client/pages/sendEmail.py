import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import threading
import streamlit as st


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
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def job():
    subject = "Workshop Count"
    count = 5
    body = "Your Workshop count is " + str(count)
    to_email = "bkasaju97@gmail.com"
    from_email = "bkasaju97@gmail.com"
    password = "ocrj owsr lvib bpmg"

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

st.title("Bulk Email Scheduler")

user_selected_day = st.selectbox("Select a day of the week:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
task_hour = st.number_input("Select hour:", min_value=0, max_value=23, value=9)
task_minute = st.number_input("Select minute:", min_value=0, max_value=59, value=0)


if st.button("Schedule"):
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    st.success("Schedule has been triggered!")



# st.write("Sends an email every Saturday at 9:00 AM.")

if st.button("Send Email"):
    job()
    st.success("Email sent!")




