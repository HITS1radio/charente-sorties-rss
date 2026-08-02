import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from dateutil import parser
import hashlib
import html

SOURCES = [
    {
        "name": "Grand Cognac",
        "url": "https://www.grand-cognac.fr/decouvrir-et-sortir/agenda-des-sorties"
    },
    {
        "name": "Destination Cognac",
        "url": "https://www.destination-cognac.com/agenda-cognac/"
    },
    {
        "name": "Agenda Culturel Charente",
        "url": "https://16.agendaculturel.fr/"
    },
    {
        "name": "Fest Charente",
        "url": "https://www.fest.fr/agenda/charente/"
    }
]


def get_events():
    events = []

    for source in SOURCES:
        try:
            r = requests.get(
                source["url"],
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            soup = BeautifulSoup(r.text, "lxml")

            for link in soup.find_all("a", href=True):
                title = link.get_text(" ", strip=True)

                if len(title) > 15:
                    events.append({
                        "title": title,
                        "source": source["name"],
                        "url": link["href"]
                    })

        except Exception as e:
            print("Erreur", source["name"], e)

    return events


def clean_events(events):

    today = datetime.now()

    result = []
    seen = set()

    for event in events:

        key = hashlib.md5(
            event["title"].encode()
        ).hexdigest()

        if key not in seen:
            seen.add(key)

            result.append(event)

    return result


def create_rss(events):

    fg = FeedGenerator()

    fg.title(
        "Sorties autour de Cognac"
    )

    fg.link(
        href="https://hits1radio.github.io/charente-sorties-rss/rss.xml"
    )

    fg.description(
        "Manifestations à venir autour de Cognac et du Grand Cognac"
    )

    for event in events[:100]:

        fe = fg.add_entry()

        fe.title(
            html.escape(event["title"])
        )

        fe.link(
            href=event["url"]
        )

        fe.description(
            f"Source : {event['source']}"
        )

        fe.pubDate(
            datetime.now(timezone.utc)
        )

    fg.rss_file(
        "rss.xml"
    )


if __name__ == "__main__":

    events = get_events()

    events = clean_events(events)

    create_rss(events)

    print(
        len(events),
        "événements générés"
    )
