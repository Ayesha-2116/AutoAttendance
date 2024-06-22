import streamlit as st
import pandas as pd
import numpy as np
import random

workshops = ["Intro to AI", "Basics of Big Data", "Information Retrieval Systems",
             "Advanced Python", "Data Visualization", "Machine Learning Basics",
             "Deep Learning", "Natural Language Processing", "Computer Vision",
             "Ethics in AI"]

first_names = ["Bivek", "Ravinder", "Happy", "Gurpreet", "Ayesha", "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan"]
last_names = ["Sharma", "Verma", "Reddy", "Patel", "Nair", "Singh", "Gupta", "Rao", "Jain", "Mehta"]


students = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(100)]

students = list(set(students))
while len(students) < 100:
    students.append(f"{random.choice(first_names)} {random.choice(last_names)}")
students = students[:100]


np.random.seed(0)
attendance_data = np.random.choice([1, 0], size=(len(students), len(workshops)))

df_attendance = pd.DataFrame(attendance_data, index=students, columns=workshops)

df_attendance['Total Workshops Attended'] = df_attendance.sum(axis=1)

df_attendance = df_attendance[['Total Workshops Attended'] + workshops]

df_attendance.replace(0, np.nan, inplace=True)

st.subheader("Workshop Attendance")
st.dataframe(df_attendance)
