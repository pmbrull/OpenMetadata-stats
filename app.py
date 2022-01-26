from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from dateutil import parser

ROOT = Path("api.github.com")
OWNER = "open-metadata"
REPO = "OpenMetadata"
HEADER = {"Accept": "application/vnd.github.v3.star+json"}

START_DATE = datetime.strptime("Aug 1 2021", "%b %d %Y")


def url(path: Path) -> str:
    return "https://" + str(path)


def get(path: Path):
    """
    Prepare a HTTPS URL from the given path
    """
    return requests.get(url(path), headers=HEADER)


def get_all(path: Path):
    """
    Return all pages from a given request
    """
    root = url(path)
    req = root + "?simple=yes&per_page=100&page=1"
    print(req)

    res = requests.get(req, headers=HEADER)
    data = res.json()
    while "next" in res.links.keys():
        res = requests.get(res.links["next"]["url"], headers=HEADER)
        data.extend(res.json())

    return data


def cook_stars_data():
    today = datetime.today()
    delta = today - START_DATE

    stars = get_all(ROOT / "repos" / OWNER / REPO / "stargazers")
    clean_stars = [
        parser.parse(user["starred_at"]).strftime("%Y/%m/%d") for user in stars
    ]
    star_counts = Counter(clean_stars)

    acc = 0
    for i in range(delta.days + 1):
        day = START_DATE + timedelta(days=i)
        day_str = day.strftime("%Y/%m/%d")
        if not star_counts.get(day_str):
            star_counts[day_str] = acc

    sorted_dict = dict(sorted(star_counts.items()))
    df = pd.DataFrame(
        {"date": list(sorted_dict.keys()), "stars": list(sorted_dict.values())}
    )

    df["date"] = pd.to_datetime(df["date"])
    df = df.resample("W", on="date")[["stars"]].sum()
    df["stars"] = df["stars"].cumsum()

    return df


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


def stats():
    st.title("OpenMetadata - Community Stats")
    cook_stars_app()


if __name__ == "__main__":
    stats()
