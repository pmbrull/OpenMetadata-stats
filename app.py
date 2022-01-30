"""
Main file to run the streamlit app
"""
import streamlit as st

from stats.components import (
    clear_cache_button,
    contributors_component,
    good_first_issues_component,
    profile_component,
    stars_component,
)


def stats():
    st.title("OpenMetadata - Community Stats")
    profile_component()
    st.markdown("---")
    stars_component()
    st.markdown("---")
    good_first_issues_component()
    st.markdown("---")
    contributors_component()
    st.markdown("---")
    clear_cache_button()


if __name__ == "__main__":
    stats()
