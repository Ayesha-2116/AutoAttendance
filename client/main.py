import streamlit as st
import Dashboard,registerStudent
import registerStudent, studentSearch, face_recognition_script
import sys, os


from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="AutoAttend Tracker",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

class AutoAttedApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title= 'Menu',
                options=[app['title'] for app in self.apps],
                icons=['house', 'pencil'],
                menu_icon='menu-app-fill',
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "#f0f2f6"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#007BFF"},
                }
            )
        for app_dict in self.apps:
            if app_dict['title'] == app:
                app_dict['function']()
                break

def display_dashboard():
    Dashboard.displayDashboard()

def register_student():
    registerStudent.runRegisterStudent()
def faceRecognition(): 
    face_recognition_script.main()
def search_Student(): 
    studentSearch.main()


app = AutoAttedApp()
app.add_app('Dashboard', display_dashboard)
app.add_app('Register Student', register_student)
app.add_app('Student Attendence', faceRecognition)
app.add_app('Student Attendence Record', search_Student)
app.run()
