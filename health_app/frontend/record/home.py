import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from health_app.frontend.components import show_go_to_meal_record_link, show_go_to_weight_record_link

from health_app.frontend.app import (
    get_user,
    get_weight_records,
    get_meals,
    delete_record,
)
from health_app.frontend.components import (
    calculate_health_indicators,
    calculate_weight_indicators,
)
from health_app.backend.schemas.meal import MealType

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

st.write("Track your daily meals,weight, and monitor your health trends.")

# TODO:認証情報をもとにユーザーIDを取得できるようにする
user_id = 5

# APIのエンドポイント
meal_record_url = "/meals/"
weight_record_url = "/weight_records/"

# ユーザー情報、食事データ、体重データを取得
if "user_data" not in st.session_state:
    st.session_state.user_data = get_user("/users/", user_id)
    
if "weight_record_df" not in st.session_state or "weight_record_updated" in st.session_state:
    weight_record_data = get_weight_records(weight_record_url, user_id)
    if weight_record_data:
        st.session_state.weight_record_df = pd.DataFrame(weight_record_data).sort_values("date")
    
if "meal_df" not in st.session_state or "meal_record_updated" in st.session_state:
    meal_data = get_meals(meal_record_url, user_id)
    if meal_data:
        st.session_state.meal_df = pd.DataFrame(meal_data).sort_values("date")
    

def delete_selected_rows(record_df, edited_record, url):
    rows_to_delete = edited_record[edited_record["delete"]].index
    
    if len(rows_to_delete) == 0:
        return
    
    # 削除の実行
    for index in rows_to_delete:
        id = record_df.iloc[index]["id"]
        delete_record(url, id)
    
    # セッションステートのデータフレームを更新
    record_df = record_df.drop(rows_to_delete).reset_index(drop=True)
    
    # 削除フラグをリセット
    record_df["delete"] = False
    
    # 更新を反映させるためにrerunを呼び出す
    st.rerun()
    
tab_weight, tab_meal = st.tabs(["Weight Record", "Meal Record"])

with tab_weight:
    if "weight_record_df" in st.session_state:
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
        show_go_to_weight_record_link()

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
        edited_weight_record = st.data_editor(
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

        # 削除ボタン
        if st.button("Delete Selected Rows", key="delete_weight_record_button", help="Delete the selected rows."):
            delete_selected_rows(st.session_state.weight_record_df, edited_weight_record, weight_record_url)
    else:
        st.write("No Data")

with tab_meal:
    if "meal_df" in st.session_state:
        col1, col2, col3 = st.columns(3)
        total_calories = 0

        # delete列を追加し、全データをfalseで初期化
        st.session_state.meal_df["delete"] = False
        
        meal_df_of_selected_day = st.session_state.meal_df[st.session_state.meal_df["date"] == str(selected_date)]
        if not meal_df_of_selected_day.empty:
            total_calories = meal_df_of_selected_day["calories"].sum()
        else:
            st.write(f"No meal data available for {selected_date}")

        col1.metric("Today's Total Calories", f"{total_calories}kcal")
        col2.metric("BMR", f"{health_indicators['BMR']}kcal")
        col3.metric(
            "Daily Caloric Needs", f"{health_indicators['Daily Caloric Needs']}kcal"
        )

        # Record Mealへのリンクを表示
        show_go_to_meal_record_link()

        if not meal_df_of_selected_day.empty:
            meal_types = [meal_type.value for meal_type in MealType]
            meal_calories = {meal_type: 0 for meal_type in meal_types}
            edited_meal_records = {}

            for meal_type in meal_types:
                meals_of_type = meal_df_of_selected_day[meal_df_of_selected_day["meal_type"] == meal_type]
                key = f"edited_meals_of_type_{meal_type}"
                
                if not meals_of_type.empty:
                    st.markdown(f"### {meal_type.capitalize()} {meals_of_type['calories'].sum()} kcal")
                    edited_meal_records[meal_type] = st.data_editor(
                        meals_of_type[["meal_name", "calories", "delete"]],
                        column_config = {
                            "delete": st.column_config.CheckboxColumn(
                                "Delete?",
                                help="Select the records you want to delete.",
                                default=False,
                            )
                        },
                        hide_index=True,
                        key=key,
                    )
                    meal_calories[meal_type] = meals_of_type["calories"].sum()
                    
            if st.button("Delete Selected Rows", key="delete_meal_record_button", help="Delete the selected rows."):
                for meal_type in meal_types:
                    if meal_type in edited_meal_records.keys():
                        delete_selected_rows(st.session_state.meal_df, edited_meal_records[meal_type], meal_record_url)

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
    else:
        st.write("No Data")