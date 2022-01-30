"""
Functions to prepare the data for
the components
"""
from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st
from dateutil import parser
from pandas import DataFrame

from stats.client import OWNER, REPO, ROOT, START_DATE, get, get_all


@st.experimental_memo
def stars_data() -> Optional[DataFrame]:
    """
    Extract information from stargazers.
    Prepare an accumulative sum of stars by date
    """
    today = datetime.today()
    delta = today - START_DATE

    try:
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

    except Exception:
        return None


@st.experimental_memo
def health_data() -> Tuple[str, str]:
    """
    Obtain the health % from the community profile
    """
    profile_data = get(ROOT / "repos" / OWNER / REPO / "community" / "profile").json()
    percentage = profile_data.get("health_percentage", "Endpoint error")
    description = profile_data.get("description", "Error fetching description")

    return percentage, description


def is_good_first_issue(issue: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Check if an issue is a good first issue
    """
    if isinstance(issue, dict):

        is_gfi = next(
            iter(
                label
                for label in issue.get("labels")
                if isinstance(label, dict) and label.get("name") == "good first issue"
            ),
            None,
        )

        return is_gfi

    return None


@st.experimental_memo
def good_first_issues_data() -> Tuple[List[dict], List[dict]]:
    """
    Analyze issues data for open and closed good
    first issues.
    """

    open_issues = get_all(ROOT / "repos" / OWNER / REPO / "issues")

    open_first_issues = [issue for issue in open_issues if is_good_first_issue(issue)]

    closed_issues = get_all(ROOT / "repos" / OWNER / REPO / "issues", "&state=closed")

    closed_first_issues = [
        issue for issue in closed_issues if is_good_first_issue(issue)
    ]

    return open_first_issues, closed_first_issues
