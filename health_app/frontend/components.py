import streamlit as st
from datetime import date

def custom_date_input(label, key, help):
    selected_date = st.date_input(
        label=label,
        key=key,
        help=help,
    )
    return selected_date.strftime("%Y-%m-%d")  # フォーマット済み文字列を返す