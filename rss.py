from feedgen.feed import FeedGenerator
import html

from utils import date_rss


def creer_flux(events):

    fg = FeedGenerator()


    fg.title(
        "Sorties autour de Cognac"
    )


    fg.link(
        href="https://hits1radio.github.io/charente-sorties-rss/rss.xml"
    )


    fg.description(
        "Manifestations et sorties autour de Cognac et du Grand Cognac"
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


        description = f"""
        <p>
        <strong>{html.escape(event['title'])}</strong>
        </p>

        <p>
        📍 Secteur Cognac
        </p>

        <p>
        Source : {html.escape(event['source'])}
        </p>

        <p>
        Retrouvez toutes les informations pratiques
        sur la page de l'événement.
        </p>
        """


        item.description(
            description
        )


        item.pubDate(
            date_rss()
        )


        item.guid(
            event["url"]
        )


    fg.rss_file(
        "rss.xml"
    )
