"""
Functions to prepare the data for
the components
"""
from collections import Counter
from datetime import datetime, timedelta

import pandas as pd
from dateutil import parser

from stats.client import START_DATE, get_all, OWNER, REPO, ROOT


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
