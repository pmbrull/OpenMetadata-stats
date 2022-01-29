"""
Module containing helper utilities
to handle Github API calls
"""
from datetime import datetime
from pathlib import Path

import requests


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
