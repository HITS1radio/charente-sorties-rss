import hashlib
from datetime import datetime, timezone


def nettoyer_texte(texte):

    if not texte:
        return ""

    return (
        texte
        .replace("\n", " ")
        .replace("\t", " ")
        .strip()
    )


def nettoyer_titre(titre):

    titre = nettoyer_texte(titre)

    morceaux = [
        " Cognac »",
        " »",
        " | Agenda"
    ]

    for morceau in morceaux:

        if morceau in titre:

            titre = titre.split(
                morceau
            )[0]


    return titre.strip()



def creer_id(titre, url):

    valeur = (
        titre
        + url
    )

    return hashlib.md5(
        valeur.encode("utf-8")
    ).hexdigest()



def supprimer_doublons(events):

    resultat = []

    vus = set()


    for event in events:

        identifiant = creer_id(
            event["title"],
            event["url"]
        )


        if identifiant in vus:
            continue


        vus.add(
            identifiant
        )

        resultat.append(
            event
        )


    return resultat



def date_rss():

    return datetime.now(
        timezone.utc
    )
