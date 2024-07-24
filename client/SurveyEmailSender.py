# SurveyEmailSender.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_survey_email(student_email, student_name, workshop_id, presenter_id):
    # Email credentials
    sender_email = "ayeshas@uwindsor.ca"
    sender_password = "test@123#"

    # Email content
    subject = "Workshop Feedback Survey"
    body = f"""
    Dear {student_name},

    Thank you for attending the workshop.

    We value your feedback and would appreciate it if you could take a few minutes to fill out our feedback survey.

    Please click on the following link to provide your feedback:
    https://<your-survey-app-url>?workshopId={workshop_id}&presenterID={presenter_id}&studentID={student_name}

    Best regards,
    Your Workshop Team
    """

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = student_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        # Use the appropriate SMTP server and port for your email provider
        session.starttls()
        session.login(sender_email, sender_password)
        text = message.as_string()
        session.sendmail(sender_email, student_email, text)
        session.quit()
        print(f"Survey email sent to {student_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
