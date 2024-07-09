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
    to_email = ""
    from_email = ""
    password = ""

    send_email(subject, body, to_email, from_email, password)

def run_scheduler():
    schedule.every().saturday.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

st.title("Email Scheduler")
st.write("Sends an email every Saturday at 9:00 AM.")

if st.button("Send Email"):
    job()
    st.success("Email sent!")
