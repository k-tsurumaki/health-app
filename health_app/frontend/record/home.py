import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

from health_app.frontend.app import get_weight_records, get_meals
from health_app.backend.schemas.meal import MealType

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

st.write("Track your daily meals,weight, and monitor your health trends.")


# DBから食事・体重データを取得
get_meal_record_url = "/meals"
meal_data = get_meals(get_meal_record_url, user_id=5)

get_weight_record_url = "/weight_records"
weight_record_data = get_weight_records(get_weight_record_url, user_id=5)


# 取得したJSON形式の食事・体重データをPandasのDataFrameに変換
meal_df = pd.DataFrame(meal_data)
weight_record_df = pd.DataFrame(weight_record_data)

# 各DataFrameをdateの昇順にソート
meal_df.sort_values("date", inplace=True)
weight_record_df.sort_values("date", inplace=True)


# PandasのDataFrameに変換したデータをグラフ化
fig = px.line(
    weight_record_df, x="date", y="weight", title="Weight Record", markers=True
)
fig.update_traces(text=weight_record_df["weight"], textposition="top center")
st.plotly_chart(fig)


# 選択された日付の食事・体重データを表示
selected_date = st.sidebar.date_input("Select a date", value=pd.Timestamp(date.today()))

selected_weights = weight_record_df[weight_record_df["date"] == str(selected_date)]
if not selected_weights.empty:
    pass
else:
    st.write(f"No weight data available for {selected_date}")

selected_meals = meal_df[meal_df["date"] == str(selected_date)]
if not selected_meals.empty:
    total_calories = 0
    meal_types = ["breakfast", "lunch", "dinner", "other"]
    meal_calories = {meal_type: 0 for meal_type in meal_types}

    for meal_type in meal_types:
        meals_of_type = selected_meals[selected_meals["meal_type"] == meal_type]
        if not meals_of_type.empty:
            st.write(f"### {meal_type.capitalize()}")
            meal_table = pd.DataFrame(meals_of_type, columns=["meal_name", "calories"])
            meal_table["calories"] = meal_table["calories"].map(
                lambda x: f"{x:.1f} kcal"
            )
            st.table(meal_table.reset_index(drop=True))
            meal_calories[meal_type] += meals_of_type["calories"].sum()
            total_calories += meals_of_type["calories"].sum()

    st.write(f"### Total calories: {total_calories} kcal")

    # 平均カロリーを計算
    avg_calories = total_calories / len(meal_types)

    # グラフを生成
    fig = go.Figure()
    for meal_type in meal_types:
        fig.add_trace(
            go.Bar(
                x=[meal_type],
                y=[meal_calories[meal_type]],
                name=meal_type.capitalize(),
                text=[f"{meal_calories[meal_type]} kcal"],
                textposition="auto",
            )
        )

    # 平均カロリーのラインを追加
    fig.add_trace(
        go.Scatter(
            x=meal_types,
            y=[avg_calories] * (len(meal_types)),
            mode="lines",
            name="Average",
            line=dict(dash="dash"),
            text=[f"{avg_calories:.1f} kcal"] * len(meal_types),
            textposition="top right",
        )
    )

    # Add total calories
    fig.add_trace(
        go.Bar(
            x=["Total"],
            y=[total_calories],
            name="Total",
            text=[f"{total_calories} kcal"],
            textposition="auto",
        )
    )

    fig.update_layout(
        title="Calories by Meal Type",
        xaxis_title="Meal Type",
        yaxis_title="Calories",
        barmode="group",
    )

    st.plotly_chart(fig)
else:
    st.write(f"No meal data available for {selected_date}")
