import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import hashlib
import html
from urllib.parse import urljoin


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


def get_events():

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

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )


            for link in soup.find_all("a", href=True):

                title = link.get_text(
                    " ",
                    strip=True
                )


                if len(title) < 15:
                    continue


                url = urljoin(
                    source["url"],
                    link["href"]
                )


                events.append(
                    {
                        "title": title,
                        "url": url
                    }
                )


        except Exception as error:

            print(
                "Erreur source :",
                source["name"],
                error
            )


    return events



def is_local(event):

    text = event["title"].lower()

    for commune in COMMUNES:

        if commune in text:
            return True

    return False



def clean_events(events):

    cleaned = []

    seen = set()


    for event in events:

        key = hashlib.md5(
            event["title"]
            .lower()
            .encode("utf-8")
        ).hexdigest()


        if key in seen:
            continue


        seen.add(key)

        cleaned.append(event)


    return cleaned



def create_rss(events):

    fg = FeedGenerator()


    fg.title(
        "Sorties autour de Cognac"
    )


    fg.link(
        href="https://hits1radio.github.io/charente-sorties-rss/rss.xml"
    )


    fg.description(
        "Les manifestations et sorties à venir autour de Cognac"
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
            <h3>{html.escape(event['title'])}</h3>

            <p>
            Découvrez cette manifestation à venir
            autour de Cognac.
            </p>

            <p>
            Retrouvez les informations pratiques :
            date, horaires, lieu et conditions d'accès
            sur la page de l'événement.
            </p>

            <p>
            Agenda local des sorties du territoire.
            </p>
            """
        )


        item.pubDate(
            datetime.now(timezone.utc)
        )


    fg.rss_file(
        "rss.xml"
    )



if __name__ == "__main__":

    print(
        "Recherche des manifestations..."
    )


    events = get_events()


    print(
        len(events),
        "éléments trouvés"
    )


    events = clean_events(
        events
    )


    print(
        len(events),
        "éléments après nettoyage"
    )


    create_rss(
        events
    )


    print(
        "Flux RSS créé avec succès"
    )
