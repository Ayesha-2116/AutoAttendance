import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.title('Auto Attend')



workshop_data = {
    "Workshop Title": [
        "Intro to AI", "Basics of Big Data", "Information Retrieval Systems",
        "Advanced Python", "Data Visualization", "Machine Learning Basics",
        "Deep Learning", "Natural Language Processing", "Computer Vision",
        "Ethics in AI"
    ],
    "Present": [36, 38, 38, 35, 37, 39, 40, 38, 36, 37],
    "Absent": [4, 2, 2, 5, 3, 1, 0, 2, 4, 3]
}


df_workshops = pd.DataFrame(workshop_data)


monthly_data = {
    "Month": ["March", "April", "May"],
    "Total Present": [1200, 1911, 1477],
    "Total Absent": [200, 9, 3]
}


df_monthly = pd.DataFrame(monthly_data)


df_monthly["Present Percentage"] = df_monthly["Total Present"] / (df_monthly["Total Present"] + df_monthly["Total Absent"]) * 100
df_monthly["Absent Percentage"] = df_monthly["Total Absent"] / (df_monthly["Total Present"] + df_monthly["Total Absent"]) * 100



late_arrival_data = {
    "Week": ["Week 1 (May 1 - 7)", "Week 2 (May 8 - 14)", "Week 3 (May 15 - 21)"],
    "Late Arrival": [12, 16, 4]
}


df_late_arrivals = pd.DataFrame(late_arrival_data)

presenter_data = {
    "Presenter": ["Aznam Yacoub", "Soroush Zadeh", "Hossein Fani", "Zara"],
    "Rating": [3, 2.5, 5, 3.5]
}


df_presenters = pd.DataFrame(presenter_data)


workshop_rating_data = {
    "Workshop": ["Intro to AI", "Basics of Big Data", "Information Retrieval Systems", "Deep Learning"],
    "Rating": [4, 3.5, 2, 4.5]
}


df_workshop_ratings = pd.DataFrame(workshop_rating_data)


col1, col2 = st.columns(2)

# Chart 1: Student attendance in workshops
with col1:
    # st.subheader("Number of Students Present and Absent in Each Workshop (Current Week)")
    fig_workshops = px.bar(df_workshops, x='Workshop Title', y=['Present', 'Absent'], barmode='group',
                           labels={'value': 'Number of Students', 'variable': 'Attendance'},
                           title='Student Attendance in Workshops')
    st.plotly_chart(fig_workshops)

# Chart 2: Monthly attendance percentages
with col2:
    # st.subheader("Present and Absent Percentage by Month")
    fig_monthly = px.bar(df_monthly, x='Month', y=['Present Percentage', 'Absent Percentage'], barmode='group',
                         labels={'value': 'Percentage', 'variable': 'Attendance'},
                         title='Monthly Attendance Percentages')
    st.plotly_chart(fig_monthly)

# Chart 3: Late arrivals in the past three weeks
with col1:
    # st.subheader("Number of Students that Arrived Late in the Past Three Weeks")
    fig_late_arrivals = px.bar(df_late_arrivals, x='Week', y='Late Arrival',
                               labels={'Late Arrival': 'Number of Students', 'Week': 'Week'},
                               title='Late Arrivals in the Past Three Weeks')
    st.plotly_chart(fig_late_arrivals)

# Chart 4: Top presenters of last week
with col2:
    # st.subheader("Top Presenters of Last Week")
    fig_presenters = px.bar(df_presenters, x='Presenter', y='Rating',
                            labels={'Rating': 'Rating', 'Presenter': 'Presenter'},
                            title='Top Presenters of Last Week')
    st.plotly_chart(fig_presenters)

# Chart 5: Top workshops of last week
with col1:
    # st.subheader("Top Workshops of Last Week")
    fig_workshop_ratings = px.bar(df_workshop_ratings, x='Workshop', y='Rating',
                                  labels={'Rating': 'Rating', 'Workshop': 'Workshop'},
                                  title='Top Workshops of Last Week')
    st.plotly_chart(fig_workshop_ratings)