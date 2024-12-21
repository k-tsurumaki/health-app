import streamlit as st
from health_app.frontend.app import post_data
from health_app.frontend.components import custom_date_input

if "current_page" not in st.session_state:
    st.session_state.current_page = "weight_record"
st.write(f"You are logged in as {st.session_state.username}.")

st.write("## 体重記録")
st.write("日付と体重を記録しよう！")

date = custom_date_input(label="日付", key="weight_record", help="日付を選択してください")
weight = st.number_input("体重 (kg)", min_value=0.0, step=0.1, format="%.1f")

if st.button("記録を保存"):
    if date and weight > 0:
        data = {"user_id": 5, "date": str(date), "weight": weight}
        post_data("/weight_records", data)
    else:
        st.warning("正しいデータを入力してください。")


