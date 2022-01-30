"""
Module creating the different streamlit
components to show on the app
"""
import altair as alt
import streamlit as st

from dataclasses import dataclass

from stats.data import (
    contributors_data,
    good_first_issues_data,
    health_data,
    stars_data,
)


@dataclass
class Style:
    primaryColor: str = "#7147E8"


def stars_component():
    """
    Prepare the graph to show the stars evolution
    and the differences
    """
    df = stars_data().reset_index(level=0)

    if df is not None and not df.empty:
        current = int(df.iloc[-1].get("stars"))
        last_week = int(df.iloc[-2].get("stars"))
        last_month = int(df.iloc[-4].get("stars"))

    else:
        st.write("Error fetching Star data")
        return

    with st.container():

        st.subheader("Stars evolution")

        line_chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X("date:T", axis=alt.Axis(tickCount=12, grid=False)),
                y="stars:Q",
                color=alt.value(Style.primaryColor),
            )
            .properties(
                width=650,
                height=350,
            )
        )

        st.altair_chart(line_chart)

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


def good_first_issues_component():
    """
    Present the good first issues
    """
    open_gfi, closed_gfi = good_first_issues_data()

    with st.container():

        st.subheader("Good first issues")

        open_issues, closed_issues, url_issues = st.columns(3)
        open_issues.metric("Open good first issues", len(open_gfi))
        closed_issues.metric("Closed good first issues", len(closed_gfi))


def clear_cache_button():
    """
    Prepare a button to clear the cached API values
    """

    with st.container():

        desc, button = st.columns(2)
        desc.write("Clear the cache to refresh the data. It may take a few seconds.")

        if button.button("Clear cache"):
            st.experimental_memo.clear()


def contributors_component():
    """
    Draw contributors data
    """

    contributors = contributors_data()

    recurrent_contributors = contributors.loc[contributors["contributions"] >= 3]

    with st.container():
        st.subheader("Contributors")

        line_chart = (
            alt.Chart(
                contributors[:10],
                title="Top 10 contributors",
            )
            .mark_bar()
            .encode(
                x=alt.X(
                    "login",
                    axis=None,
                    sort=alt.EncodingSortField(
                        field="contributions", op="count", order="descending"
                    ),
                ),
                y=alt.Y("contributions"),
                color=alt.value(Style.primaryColor),
            )
            .properties(
                width=650,
                height=350,
            )
        )

        st.altair_chart(line_chart)

        total, recurrent = st.columns(2)
        total.metric("Total contributors", contributors.shape[0])
        recurrent.metric("Recurrent contributors", recurrent_contributors.shape[0])
