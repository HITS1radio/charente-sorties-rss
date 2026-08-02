import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils import nettoyer_titre, nettoyer_texte


URL = "https://www.fest.fr/agenda/charente/cognac"


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
    "guide"
]


if any(
    mot in url.lower()
    for mot in EXCLUS
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


            if "fest.fr" not in url:
                continue


if "-20" not in url:
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
