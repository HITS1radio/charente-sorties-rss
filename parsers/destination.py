import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils import nettoyer_titre


URL = "https://www.destination-cognac.com/agenda-cognac/tout-lagenda/"


def recuperer_destination():

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


            titre = lien.get_text(
                " ",
                strip=True
            )


            titre = nettoyer_titre(
                titre
            )


            if len(titre) < 10:
                continue


            if "agenda" not in url.lower():
                continue


            events.append(
                {
                    "title": titre,
                    "url": url,
                    "description": "",
                    "source": "Destination Cognac"
                }
            )


    except Exception as erreur:

        print(
            "Erreur Destination Cognac :",
            erreur
        )


    return events
