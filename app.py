"""
Main file to run the streamlit app
"""
import streamlit as st

from stats.components import stars_component, profile_component, good_first_issues, clear_cache_button


def stats():
    st.title("OpenMetadata - Community Stats")
    profile_component()
    st.markdown("---")
    stars_component()
    st.markdown("---")
    good_first_issues()
    st.markdown("---")
    clear_cache_button()


if __name__ == "__main__":
    stats()

# TODO: Auth and pass secrets to the app to increase the API rate limit
# https://blog.streamlit.io/secrets-in-sharing-apps/
