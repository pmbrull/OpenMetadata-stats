"""
Main file to run the streamlit app
"""
import streamlit as st

from stats.components import cook_stars_app


def stats():
    st.title("OpenMetadata - Community Stats")
    cook_stars_app()


if __name__ == "__main__":
    stats()
