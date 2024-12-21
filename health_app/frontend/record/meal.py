import streamlit as st
from PIL import Image
from health_app.frontend.app import post_data
from health_app.frontend.components import custom_date_input

if "current_page" not in st.session_state:
    st.session_state.current_page = "meal"
    
st.write(f"You are logged in as {st.session_state.username}.")

st.write("## 食事記録")
st.write("日付と食事を記録しよう！")

date = custom_date_input(label="日付", key="meal_record", help="日付を選択してください")
meal_type = st.selectbox(
"食事の種類を選択", options=["breakfast", "lunch", "dinner", "other"], index=0
)
meal_name = st.text_input("食べた料理を入力")
calories = st.number_input("カロリーを入力(kcal)", min_value=0.0, step=1.0)

uploaded_image = st.file_uploader(
"食事の画像をアップロード", type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="アップロードされた食事の画像")

else:
    st.warning("画像をアップロードしてください")

if st.button("送信"):
    if not meal_name:
        st.error("食品名を入力してください")
    elif calories<0:
        st.error("カロリーを正しく入力してください")
    else:
        data = {
            "user_id": 5,
            "meal_type": meal_type,
            "meal_name": meal_name,
            "calories": calories,
            "date": date
        }
        post_data("/meals/", data)

