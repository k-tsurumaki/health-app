import streamlit as st
from PIL import Image
from health_app.frontend.app import post_data
from health_app.frontend.components import custom_date_input

if "current_page" not in st.session_state:
    st.session_state.current_page = "meal"
    
st.write(f"You are logged in as {st.session_state.username}.")

st.write("## Meal Record")
st.write("Let's record the date and meal!")

date = custom_date_input(label="Date", key="meal_record", help="Please select a date")
meal_type = st.selectbox(
    "Select meal type", options=["breakfast", "lunch", "dinner", "other"], index=0
)
meal_name = st.text_input("Enter the meal name")
calories = st.number_input("Enter calories (kcal)", min_value=0.0, step=1.0)

uploaded_image = st.file_uploader(
    "Upload meal image", type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded meal image")

else:
    st.warning("Please upload an image")

if st.button("Submit"):
    if not meal_name:
        st.error("Please enter the meal name")
    elif calories < 0:
        st.error("Please enter valid calories")
    else:
        data = {
            "user_id": 5,
            "meal_type": meal_type,
            "meal_name": meal_name,
            "calories": calories,
            "date": date
        }
        post_data("/meals/", data)