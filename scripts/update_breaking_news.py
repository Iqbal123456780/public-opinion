#!/usr/bin/env python3
"""Build a small, source-linked Pakistan political headlines feed from publisher RSS."""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse

FEEDS = [
    ("Dawn", "https://www.dawn.com/feeds/pakistan/"),
    ("The Express Tribune", "https://tribune.com.pk/feed/home"),
    ("The News International", "https://www.thenews.com.pk/rss/1/1"),
    ("The Nation", "https://nation.com.pk/rss/top-stories"),
]
POLITICAL_TERMS = re.compile(
    r"\b(pakistan|pti|imran khan|khan|pml\-n|pmln|ppp|bilawal|nawaz|"
    r"shehbaz|asif zardari|maryam|parliament|senate|national assembly|"
    r"election|minister|government|cabinet|court|supreme court|"
    r"high court|politic|constitution|islamabad|protest|assembly|"
    r"opposition|jail|detention|letter|statement|mna|mpa)\b",
    re.IGNORECASE,
)
OUT = Path("breaking-news.json")
NOW = datetime.now(timezone.utc)
CUTOFF = NOW - timedelta(hours=72)


def local_name(tag):
    return tag.rsplit("}", 1)[-1].lower()


def child_text(node, names):
    for child in list(node):
        if local_name(child.tag) in names:
            if child.text:
                return child.text.strip()
            for key, value in child.attrib.items():
                if key.lower() == "href":
                    return value.strip()
    return ""


def parse_date(value):
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError, OverflowError):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            return None


def get_items(source, feed_url):
    request = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "PublicOpinionNewsBot/1.0 (+https://iqbal123456780.github.io/public-opinion/)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = response.read(4_000_000)
        root = ET.fromstring(payload)
    except Exception as exc:
        print(f"Feed unavailable: {source}: {exc}")
        return []

    found = []
    for node in root.iter():
        if local_name(node.tag) not in ("item", "entry"):
            continue
        title = child_text(node, {"title"})
        link = child_text(node, {"link"})
        if not link:
            for child in list(node):
                if local_name(child.tag) == "link":
                    link = child.attrib.get("href", "").strip()
                    if link:
                        break
        date_text = child_text(node, {"pubdate", "published", "updated", "date"})
        published = parse_date(date_text) or NOW
        if not title or not link or not link.startswith(("https://", "http://")):
            continue
        if not POLITICAL_TERMS.search(title):
            continue
        if published < CUTOFF or published > NOW + timedelta(hours=2):
            continue
        domain = urlparse(link).netloc.lower()
        if not domain:
            continue
        found.append({
            "title": re.sub(r"\s+", " ", title).strip(),
            "url": link,
            "source": source,
            "published": published.isoformat().replace("+00:00", "Z"),
        })
    return found


def main():
    all_items = []
    for source, url in FEEDS:
        all_items.extend(get_items(source, url))

    unique = {}
    for item in all_items:
        key = item["url"].split("#", 1)[0].rstrip("/")
        unique.setdefault(key, item)

    items = sorted(
        unique.values(),
        key=lambda item: item["published"],
        reverse=True,
    )[:20]

    payload = {
        "updated_at": NOW.isoformat().replace("+00:00", "Z"),
        "items": items,
        "sources": [source for source, _ in FEEDS],
        "note": "Headlines are reproduced as source titles and link to the original publisher. Public Opinion News does not independently verify each headline.",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} source-linked political headlines.")


if __name__ == "__main__":
    main()
