import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
from urllib.parse import urljoin
import hashlib
import html


SOURCES = [
    {
        "name": "Fest Charente",
        "url": "https://www.fest.fr/agenda/charente/"
    }
        {
        "name": "Destination Cognac",
        "url": "https://www.destination-cognac.com/agenda-cognac/"
    },
    {
        "name": "Agenda Culturel Charente",
        "url": "https://16.agendaculturel.fr/"
    },
]


MOTS_EXCLUS = [
    "installer",
    "application",
    "faq",
    "conditions",
    "confidentialite",
    "confidentialité",
    "mentions",
    "regles",
    "règles",
    "connexion",
    "inscription",
    "politique",
    "guide",
    "email",
    "recevoir",
    "newsletter",
    "cgv",
    "charente-maritime",
    "pyrenees",
    "agenda/charente"
]


def nettoyer_titre(title):

    title = title.replace(
        "\n",
        " "
    ).strip()


    if " » " in title:

        title = title.split(
            " » "
        )[0]


    return title



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


            for link in soup.find_all(
                "a",
                href=True
            ):

                title = link.get_text(
                    " ",
                    strip=True
                )


                title = nettoyer_titre(
                    title
                )


                url = urljoin(
                    source["url"],
                    link["href"]
                )


                texte = (
                    title.lower()
                    + " "
                    + url.lower()
                )


                if any(
                    mot in texte
                    for mot in MOTS_EXCLUS
                ):
                    continue


                if len(title) < 15:
                    continue


                # Garder uniquement les fiches événements Fest.fr
                if "fest.fr" in url:

                    dernier = url.split("-")[-1]

                    if not dernier.replace(
                        ".html",
                        ""
                    ).isdigit():

                        continue


                events.append(
                    {
                        "title": title,
                        "url": url
                    }
                )


        except Exception as error:

            print(
                "Source ignorée :",
                source["name"],
                error
            )


    return events



def clean_events(events):

    result = []

    seen = set()


    for event in events:

        cle = hashlib.md5(
            event["title"]
            .lower()
            .encode("utf-8")
        ).hexdigest()


        if cle in seen:
            continue


        seen.add(cle)

        result.append(
            event
        )


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
        "Manifestations et sorties à venir autour de Cognac"
    )


    for event in events[:100]:

        item = fg.add_entry()


        item.title(
            html.escape(
                event["title"]
            )
        )


        # Pas de balise link volontairement


        item.description(
            f"""
            <p>
            <strong>
            {html.escape(event['title'])}
            </strong>
            </p>

            <p>
            Manifestation à venir autour de Cognac.
            </p>

            <p>
            Retrouvez les informations pratiques
            de cette sortie auprès de l'organisateur.
            </p>

            """
        )


        item.pubDate(
            datetime.now(
                timezone.utc
            )
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
        "événements trouvés"
    )


    events = clean_events(
        events
    )


    print(
        len(events),
        "événements après nettoyage"
    )


    create_rss(
        events
    )


    print(
        "Flux RSS créé avec succès"
    )
