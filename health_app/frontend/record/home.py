import streamlit as st

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

st.write("Track your daily meals,weight, and monitor your health trends.")

# get_users_button = st.button("Get All Users Info")

# if get_users_button:
#     url = "http://127.0.0.1:8000/api/v1/users/"
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()
#         st.write(data)
