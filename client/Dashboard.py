import streamlit as st
import pandas as pd
import plotly.express as px

#st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

def displayDashboard():
    
    
    st.title('Auto Attend')

    #CHART No.1 : ---------------------------------
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

    #Removed the Monthly data showcasing the attendance count per workshop.
    #Will add it in the end if needed.

    #CHART No.2 : ---------------------------------
    late_arrival_data = {
        "Workshop Title": [
        "Intro to AI", "Basics of Big Data", "Information Retrieval Systems",
        "Advanced Python", "Data Visualization", "Machine Learning Basics",
        "Deep Learning", "Natural Language Processing", "Computer Vision",
        "Ethics in AI"
        ],
        "Late Arrival": [12, 4, 16, 1, 1, 3, 7, 2, 5, 13]
    }


    df_late_arrivals = pd.DataFrame(late_arrival_data)

    #CHART No.3 : ---------------------------------
    #previous week
    presenter_data = {
        "Presenter": ["Aznam Yacoub", "Soroush Zadeh", "Hossein Fani", "Zara"],
        "Rating": [3, 2.5, 5, 3.5]
    }


    df_presenters = pd.DataFrame(presenter_data)

    #CHART No.4 : ---------------------------------
    #previous week
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
                            title="Student's Attendance in Workshops")
        st.plotly_chart(fig_workshops)

    # Chart 2: Late arrivals in the past three weeks
    with col2:
        # st.subheader("Number of Students that Arrived Late in the Past Three Weeks")
        fig_late_arrivals = px.bar(df_late_arrivals, x='Workshop Title', y='Late Arrival',
                                labels={'Late Arrival': 'Number of Students', 'Workshop Title': 'Workshop Title'},
                                title='Late Arrivals')
        fig_late_arrivals.update_traces(marker_color='orange')
        st.plotly_chart(fig_late_arrivals)

    # Chart 3: Top presenters of last week
    with col1:
        # st.subheader("Top Presenters of Last Week")
        fig_presenters = px.pie(
            df_presenters,
            names='Presenter',
            values='Rating',
            labels={'Rating': 'Rating', 'Presenter': 'Presenter'},
            title='Top Presenters of Last Week'
        )
        st.plotly_chart(fig_presenters)

    # Chart 4: Top workshops of last week
    with col2:
        fig_workshop_ratings = px.pie(
            df_workshop_ratings,
            names='Workshop',
            values='Rating',
            labels={'Rating': 'Rating', 'Workshop': 'Workshop'},
            title='Top Workshops of Last Week',
            color_discrete_sequence=px.colors.qualitative.Light24

        )
        st.plotly_chart(fig_workshop_ratings)

displayDashboard()