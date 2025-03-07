import streamlit as st
from health_app.frontend.app import post_data
from health_app.frontend.components import custom_date_input, show_back_to_dashboard_link

if "current_page" not in st.session_state:
    st.session_state.current_page = "weight_record"
if "wight_record_updated" not in st.session_state:
    st.session_state.weight_record_updated = False
    
st.write(f"You are logged in as {st.session_state.username}.")

st.write("## Weight Record")
st.write("Let's record the date and weight!")

date = custom_date_input(label="Date", key="weight_record", help="Please select a date")
weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, format="%.1f")

if st.button("Save Record"):
    if date and weight > 0:
        data = {"user_id": 5, "date": str(date), "weight": weight}
        post_data("/weight_records", data)
        st.session_state.weight_record_updated = True
    else:
        st.error("Please enter valid data.")
        
# Dashboardへのリンクを表示
show_back_to_dashboard_link()