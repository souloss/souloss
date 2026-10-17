"""Small GitHub REST client for public profile data."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor


API = "https://api.github.com"


def repositories(username):
    """Return all owner repositories, following pagination and sorting by last push."""
    username = urllib.parse.quote(username, safe="")
    url = f"{API}/users/{username}/repos?type=owner&sort=pushed&direction=desc&per_page=100&page=1"
    items = []
    while url:
        request = urllib.request.Request(url, headers=_headers())
        page, url = _get_page(request)
        items.extend(page)
    return items


def language_totals(repositories):
    """Aggregate GitHub's per-repository language byte counts."""
    urls = [repo["languages_url"] for repo in repositories if repo.get("languages_url")]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = pool.map(_json_url, urls)

    totals = {}
    for language_map in results:
        for language, size in language_map.items():
            totals[language] = totals.get(language, 0) + int(size)
    return totals


def _headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "souloss-profile-panel",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _get_page(request, retries=3):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.load(response)
                next_url = _next_link(response.headers.get("Link", ""))
                return data, next_url
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def _json_url(url, retries=3):
    request = urllib.request.Request(url, headers=_headers())
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def _next_link(header):
    for entry in header.split(","):
        if 'rel="next"' in entry:
            return entry[entry.find("<") + 1:entry.find(">")]
    return None
