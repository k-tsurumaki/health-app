import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from st_aggrid import AgGrid

from health_app.frontend.app import (
    get_user,
    get_weight_records,
    get_meals,
    delete_weight_record,
)
from health_app.frontend.components import (
    calculate_health_indicators,
    calculate_weight_indicators,
)
from health_app.backend.schemas.meal import MealType

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

st.write("Track your daily meals,weight, and monitor your health trends.")

user_id = 5
meal_record_url = "/meals/"
weight_record_url = "/weight_records/"

if "user_data" not in st.session_state:
    st.session_state.user_data = get_user("/users/", user_id)

if "meal_df" not in st.session_state:
    meal_data = get_meals(meal_record_url, user_id)
    st.session_state.meal_df = pd.DataFrame(meal_data).sort_values("date")
    
if "weight_record_df" not in st.session_state or "weight_record_updated" in st.session_state:
    weight_record_data = get_weight_records(weight_record_url, user_id)
    st.session_state.weight_record_df = pd.DataFrame(weight_record_data).sort_values("date")

tab_weight, tab_meal = st.tabs(["Weight Record", "Meal Record"])

with tab_weight:
    # 各指標を取得
    weight_indicators = calculate_weight_indicators(st.session_state.user_data["height_cm"])
    health_indicators = calculate_health_indicators(
        st.session_state.user_data["age"],
        st.session_state.user_data["height_cm"],
        st.session_state.weight_record_df.iloc[-1]["weight"],
        st.session_state.user_data["gender"],
    )
    weight_indicators_df = pd.DataFrame(weight_indicators, index=[0])
    health_indicators_df = pd.DataFrame(health_indicators, index=[0])

    weight_delta = (
        st.session_state.weight_record_df.iloc[-1]["weight"] - st.session_state.weight_record_df.iloc[-2]["weight"]
    )

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Weight", f"{st.session_state.weight_record_df.iloc[-1]['weight']}kg", f"{weight_delta:.1f} kg"
    )
    col2.metric("BMI", health_indicators["BMI"])
    col3.metric("Obesity Degree", health_indicators["Obesity Degree"])

    # Record Weightへのリンクを表示
    st.page_link(
        "record/weight_record.py",
        label="Record today's weight",
        icon=":material/fitness_center:",
    )

    # 選択された日付の食事・体重データを表示
    selected_date = st.sidebar.date_input(
        "Select a date", value=pd.Timestamp(date.today())
    )

    # PandasのDataFrameに変換したデータをグラフ化
    fig = go.Figure()

    # 体重データのラインを追加
    fig.add_trace(
        go.Scatter(
            x=st.session_state.weight_record_df["date"],
            y=st.session_state.weight_record_df["weight"],
            mode="lines+markers+text",
            name="Weight",
            text=st.session_state.weight_record_df["weight"],
            textposition="bottom center",
            line=dict(color="#BC2A2D"),
        )
    )

    # weight_indicatorsの3つの指標を追加
    colors = ["#DBDFEA", "#92A0BF", "#52648C"]
    for i, (indicator, value) in enumerate(weight_indicators.items()):
        fig.add_hline(
            y=value,
            line_dash="dash",
            annotation_text=f"{indicator}: {value}kg",
            annotation_position="top right",
            line_color=colors[i % len(colors)],
            name=indicator,  # 凡例に指標の名前を追加
        )

    # 凡例を表示
    fig.update_layout(xaxis_title="Date", yaxis_title="Weight [kg]", showlegend=True)

    st.plotly_chart(fig)

    # delete列を追加し、全データをfalseで初期化
    st.session_state.weight_record_df["delete"] = False

    # st.session_state.weight_record_dfのdate列とweight列、delete列を表示
    edited_weight_record_df = st.data_editor(
        st.session_state.weight_record_df[["date", "weight", "delete"]],
        column_config={
            "delete": st.column_config.CheckboxColumn(
                "Delete?",
                help="Select the records you want to delete.",
                default=False,
            )
        },
        disabled=["date", "weight"],
        hide_index=True,
        key="edited_weight_record_df",
    )
    
    def delete_selected_rows():
        rows_to_delete = edited_weight_record_df[edited_weight_record_df["delete"]].index
        
        # 削除の実行
        for index in rows_to_delete:
            id = st.session_state.weight_record_df.iloc[index]["id"]
            delete_weight_record(weight_record_url, id)
        
        # セッションステートのデータフレームを更新
        st.session_state.weight_record_df = st.session_state.weight_record_df.drop(rows_to_delete).reset_index(drop=True)
        
        # 削除フラグをリセット
        st.session_state.weight_record_df["delete"] = False
        
        # 更新を反映させるためにrerunを呼び出す
        st.rerun()
        

    # 削除ボタン
    if st.button("Delete Selected Rows"):
        delete_selected_rows()

with tab_meal:
    col1, col2, col3 = st.columns(3)
    total_calories = 0

    selected_meals = st.session_state.meal_df[st.session_state.meal_df["date"] == str(selected_date)]
    if not selected_meals.empty:
        total_calories = selected_meals["calories"].sum()
    else:
        st.write(f"No meal data available for {selected_date}")

    col1.metric("Today's Total Calories", f"{total_calories}kcal")
    col2.metric("BMR", f"{health_indicators['BMR']}kcal")
    col3.metric(
        "Daily Caloric Needs", f"{health_indicators['Daily Caloric Needs']}kcal"
    )

    # Record Mealへのリンクを表示
    st.page_link(
        "record/meal.py",
        label="Record today's meals",
        icon=":material/restaurant:",
    )

    selected_meals = st.session_state.meal_df[st.session_state.meal_df["date"] == str(selected_date)]
    if not selected_meals.empty:
        meal_types = ["breakfast", "lunch", "dinner", "other"]
        meal_calories = {meal_type: 0 for meal_type in meal_types}

        for meal_type in meal_types:
            meals_of_type = selected_meals[selected_meals["meal_type"] == meal_type]
            if not meals_of_type.empty:
                st.markdown(f"### {meal_type.capitalize()}")
                meal_table = pd.DataFrame(
                    meals_of_type, columns=["meal_name", "calories"]
                )
                meal_table["calories"] = meal_table["calories"].map(
                    lambda x: f"{x:.1f} kcal"
                )
                st.dataframe(meal_table.reset_index(drop=True))
                meal_calories[meal_type] += meals_of_type["calories"].sum()

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
            xaxis_title="Meal Type",
            yaxis_title="Calories [kcal]",
            barmode="group",
        )

        st.plotly_chart(fig)
