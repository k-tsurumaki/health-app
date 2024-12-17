import streamlit as st
import requests
from datetime import datetime, date

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

st.title("Health Management")
st.write("Track your daily meals,weight, and monitor your health trends.")

get_users_button = st.button("Get All Users Info")

if get_users_button:
    url = "http://127.0.0.1:8000/api/v1/users/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        st.write(data)


# weight = st.number_input("Enter Your Weight (kg)", min_value=1.0, max_value=200.0, step=0.1)

# submit_button = st.button("Save Weight")

# if submit_button:
#     data = {
#         "weight": weight,
#         "date_time": datetime.now()
#     }
