import streamlit as st
from health_app.frontend.app import post_data
from health_app.frontend.style import set_page_config, set_custom_css
from health_app.frontend.components import custom_date_input


def record_weight_page():
    set_page_config()
    set_custom_css()

    st.title("体重記録ページ 📝")
    st.write("日付と体重を記録しよう！")

    date = custom_date_input()
    weight = st.number_input("体重 (kg)", min_value=0.0, step=0.1, format="%.1f")

    if st.button("記録を保存"):
        if date and weight > 0:
            data = {"user_id": 5, "date": str(date), "weight": weight}
            post_data("/weight_records", data)
        else:
            st.warning("正しいデータを入力してください。")


if __name__ == "__main__":
    record_weight_page()
