import streamlit as st

# 日付入力の共通関数
def custom_date_input():
    return st.date_input(
        label="日付",  # ラベルを明示
        key="date_input",
        help="記録したい日付をカレンダーから選んでください"
    )