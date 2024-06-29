import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
URI = "mongodb+srv://AutoAttendNew:AutoAttendNew@cluster0.vlu3rze.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = 'attendance_system'

def connect_to_mongodb(uri):
    """
    Establishes a connection to MongoDB and returns the database and required collections.
    """
    client = MongoClient(uri)
    db = client[DB_NAME]
    return db, db['ratings']

def main():
    st.title("Workshop Feedback Survey")
    st.header("We value your feedback!")

    # Connect to MongoDB
    db, feedback_collection = connect_to_mongodb(URI)

    # Survey form
    with st.form("feedback_form"):
        name = st.text_input("Name")
        studentID = st.text_input("Student ID")
        workshopId = st.text_input("Workshop ID")
        presenterID = st.text_input("Presenter ID")
        comments = st.text_area("Comments on the workshop content")

        st.markdown("### Rate the workshop and presenter")
        workshop_rating = st.slider("Workshop Rating", 1, 5, 3)
        presenter_rating = st.slider("Presenter Rating", 1, 5, 3)

        # Submit button
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Prepare the rating details
        rating_details = {
            "studentID": studentID,
            "workshopId": workshopId,
            "presenterID": presenterID,
            "workshop_rating": workshop_rating,
            "presenter_rating": presenter_rating,
            "comments": comments,
            "date": datetime.utcnow()
        }

        # Insert the rating details into MongoDB
        feedback_collection.insert_one(rating_details)

        st.success("Thank you for your feedback!")
        st.balloons()

    # Display the form details (optional, for debugging or review purposes)
    if submitted:
        st.write("### Submitted Feedback")
        #st.json(rating_details)

if __name__ == "__main__":
    main()