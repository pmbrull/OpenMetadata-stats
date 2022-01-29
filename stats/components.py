"""
Module creating the different streamlit
components to show on the app
"""
import streamlit as st

from stats.data import stars_data, health_data, good_first_issues_data


def stars_component():
    """
    Prepare the graph to show the stars evolution
    and the differences
    """
    df = stars_data()

    if df is not None and not df.empty:
        current = int(df.iloc[-1].get("stars"))
        last_week = int(df.iloc[-2].get("stars"))
        last_month = int(df.iloc[-4].get("stars"))

    else:
        st.write("Error fetching Star data")
        return

    with st.container():

        st.subheader("Stars evolution")
        st.line_chart(df)

        star_current, star_weekly, star_monthly = st.columns(3)
        star_current.metric("Current stars", current)
        star_weekly.metric("Last week inc.", last_week, current - last_week)
        star_monthly.metric("Last month inc.", last_month, current - last_month)


def profile_component():
    """
    Show the health % and project description
    """

    percentage, desc = health_data()

    with st.container():

        health_col, desc_col = st.columns(2)
        health_col.metric("Health %", f"{percentage}%")
        desc_col.info(desc)


def good_first_issues():
    """
    Present the good first issues
    """
    open_gfi, closed_gfi = good_first_issues_data()

    with st.container():

        st.subheader("Good first issues")

        open_issues, closed_issues, url_issues = st.columns(3)
        open_issues.metric("Open good first issues", len(open_gfi))
        closed_issues.metric("Closed good first issues", len(closed_gfi))
