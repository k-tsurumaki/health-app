import streamlit as st
import time
from health_app.frontend.components import format_page_title


def login():
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        with st.spinner("Logging in..."):
            success = _authenticate(username, password)
            if success:
                st.session_state.current_page = "home"
                st.session_state.username = username
                time.sleep(2)
                st.rerun()
            else:
                st.write("Invalid Username or Password")
            _authenticate(username, password)
            
def _authenticate(username, password):
    if username == "admin" and password == "admin":
        return True
    return False
        

def logout():
    st.session_state.current_page = "main"
    st.session_state.username = ""
    st.rerun()


# session_stateにcurrent_pageが存在しなかったら作成し、mainで初期化
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"

if "username" not in st.session_state:
    st.session_state.username = ""

current_page = st.session_state.current_page

logout_page = st.Page(logout, title=format_page_title("Logout"), icon=":material/logout:")
settings = st.Page("settings.py", title=format_page_title("Settings"), icon=":material/settings:")
home_page = st.Page(
    "record/home.py", title=format_page_title("Dashboard"), icon=":material/dashboard:", default=(current_page == "home")
)
record_meal_page = st.Page("record/meal.py", title=format_page_title("Record Meal"), icon=":material/restaurant:")
record_weight_page = st.Page(
    "record/weight_record.py", title=format_page_title("Record Weight"), icon=":material/fitness_center:"
)

accout_pages = [logout_page, settings]
home_page = [home_page]
record_pages = [record_meal_page, record_weight_page]

st.title("Health Tracker 💪")

if st.session_state.current_page == "home":
    pg = st.navigation(
        {"Account": accout_pages, "Dashboard": home_page, "Record": record_pages}
    )
else:
    pg = st.navigation([st.Page(login, title=format_page_title("Login"), icon=":material/login:")])

pg.run()