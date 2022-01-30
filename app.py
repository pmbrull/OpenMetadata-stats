"""
Main file to run the streamlit app
"""
import streamlit as st

from stats.components import (
    clear_cache_button,
    contributors_component,
    good_first_issues_component,
    stars_component, traffic_component, sidebar,
)


def stats():
    st.title("OpenMetadata - Community Stats")
    sidebar()
    stars_component()
    st.markdown("---")
    good_first_issues_component()
    st.markdown("---")
    contributors_component()
    st.markdown("---")
    traffic_component()


if __name__ == "__main__":
    stats()
