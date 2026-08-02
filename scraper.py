import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from dateutil import parser
import hashlib
import html
import re


SOURCES = [
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


COMMUNES = [
    "cognac",
    "chateaubernard",
    "châteaubernard",
    "jarnac",
    "segonzac",
    "cherves",
    "cherves-richemont",
    "merpins",
    "boutiers",
    "bourg-charente",
    "gensac",
    "saint-laurent"
]


def get_pages():

    events = []

    for source in SOURCES:

        try:

            response = requests.get(
                source["url"],
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            for link in soup.find_all("a", href=True):

                title = link.get_text(
                    " ",
                    strip=True
                )

                if len(title) < 10:
                    continue

                url = link["href"]

                if url.startswith("/"):
                    url = source["url"].split("/",3)[0] + "//" + source["url"].split("/",3)[2] + url


                events.append(
                    {
                        "title": title,
                        "url": url,
                        "source": source["name"]
                    }
                )

        except Exception as error:

            print(
                source["name"],
                error
            )


    return events



def is_local(event):

    text = (
        event["title"]
        .lower()
    )

    return any(
        commune in text
        for commune in COMMUNES
    )



def clean(events):

    today = datetime.now(
        timezone.utc
    )

    final = []
    seen = set()


    for event in events:

        key = hashlib.md5(
            event["title"].lower().encode()
        ).hexdigest()


        if key in seen:
            continue


        seen.add(key)


        final.append(event)


    return final



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

        item = fg.add_entry()

        item.title(
            html.escape(
                event["title"]
            )
        )

        item.link(
            href=event["url"]
        )

        item.description(
            f"""
            Manifestation locale<br>
            Source : {event['source']}
            """
        )

        item.pubDate(
            datetime.now(timezone.utc)
        )


    fg.rss_file(
        "rss.xml"
    )



if __name__ == "__main__":

    events = get_pages()

    events = clean(events)

    create_rss(events)

    print(
        len(events),
        "événements générés"
    )
