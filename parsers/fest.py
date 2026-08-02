import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils import nettoyer_titre


URL = "https://www.fest.fr/agenda/charente/cognac"


EXCLUS = [
    "installation",
    "contact",
    "faq",
    "cgv",
    "confidentialite",
    "mentions",
    "regles",
    "politique",
    "newsletter",
    "guide",
    "agenda-email"
]


def recuperer_fest():

    events = []

    try:

        response = requests.get(
            URL,
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


        for lien in soup.find_all(
            "a",
            href=True
        ):

            url = urljoin(
                URL,
                lien["href"]
            )


            # Suppression des pages inutiles Fest
            if any(
                mot in url.lower()
                for mot in EXCLUS
            ):
                continue


            # Garder uniquement les fiches événements
            if not url.endswith(".html"):
                continue


            if not any(
                caractere.isdigit()
                for caractere in url
            ):
                continue


            titre = lien.get_text(
                " ",
                strip=True
            )


            titre = nettoyer_titre(
                titre
            )


            if len(titre) < 10:
                continue


            events.append(
                {
                    "title": titre,
                    "url": url,
                    "description": "",
                    "source": "Fest"
                }
            )


    except Exception as erreur:

        print(
            "Erreur Fest :",
            erreur
        )


    return events
