import streamlit as st
import pandas as pd
import plotly.express as px

from health_app.frontend.app import BASE_URL, get_weight_records

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

st.write("Track your daily meals,weight, and monitor your health trends.")

# DBから体重データを取得
get_weight_record_url = "/weight_records/"
data = get_weight_records(get_weight_record_url, user_id=5)

# 取得したJSON形式の体重データをPandasのDataFrameに変換
df = pd.DataFrame(data)

# PandasのDataFrameに変換したデータをグラフ化
fig = px.line(df, x="date", y="weight", title="Weight Record")
st.plotly_chart(fig)
