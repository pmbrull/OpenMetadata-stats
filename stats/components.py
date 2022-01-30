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
    stars_data, traffic_data,
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

        st.write("Clear the cache to refresh the data. It may take a few seconds.")

        if st.button("Clear cache"):
            st.experimental_memo.clear()


def contributors_component():
    """
    Draw contributors data
    """

    contributors = contributors_data()

    recurrent_contributors = contributors.loc[contributors["contributions"] >= 3]

    with st.container():
        st.subheader("Contributors")

        bars = (
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
        )

        text = bars.mark_text(
            align='center',
            baseline='middle',
            fontSize=13,
            dy=-8  # Nudges text to top so it doesn't appear on top of the bar
        ).encode(
                text="contributions:Q",
            )

        chart = (bars + text).properties(
                width=650,
                height=350,
            )

        st.altair_chart(chart)

        total, recurrent = st.columns(2)
        total.metric("Total contributors", contributors.shape[0])
        recurrent.metric("Recurrent contributors", recurrent_contributors.shape[0])


def traffic_component():
    """
    Show clones and project views for the last 14 days
    """

    clones, views = traffic_data()

    with st.container():
        st.subheader("Traffic for the last 14 days")

        clones_col, views_col = st.columns(2)
        clones_col.metric("# Unique Clones", clones)
        views_col.metric("# Unique Views", views)


def profile_component():
    percentage, desc = health_data()

    st.write(desc)
    social_component()
    st.markdown("---")
    st.metric("Repository Health %", f"{percentage}%")


def social_component():

    social = """
    Come and say hi 👋
    
    [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/open-metadata/OpenMetadata)
    [![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://slack.open-metadata.org/)
    """
    st.markdown(social)


def sidebar():

    with st.sidebar.container():
        st.image("./assets/openmetadata.png")
        st.write("\n\n")

        profile_component()
        st.markdown("---")
        clear_cache_button()
