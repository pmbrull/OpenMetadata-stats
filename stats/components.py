"""
Module creating the different streamlit
components to show on the app
"""
import streamlit as st

from stats.data import cook_stars_data


def cook_stars_app():
    df = cook_stars_data()

    current = int(df.iloc[-1].get("stars"))
    last_week = int(df.iloc[-2].get("stars"))
    last_month = int(df.iloc[-4].get("stars"))

    st.subheader("Stars evolution")
    st.line_chart(df)

    star_current, star_weekly, star_monthly = st.columns(3)
    star_current.metric("Current stars", current)
    star_weekly.metric("Last week inc.", last_week, current - last_week)
    star_monthly.metric("Last month inc.", last_month, current - last_month)
