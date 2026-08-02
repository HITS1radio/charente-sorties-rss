from parsers.fest import recuperer_fest
from parsers.destination import recuperer_destination

from utils import supprimer_doublons

from rss import creer_flux



def main():

    print(
        "Recherche des manifestations..."
    )


    events = []


    fest = recuperer_fest()

    print(
        "Fest :",
        len(fest)
    )


    events.extend(
        fest
    )


    destination = recuperer_destination()

    print(
        "Destination Cognac :",
        len(destination)
    )


    events.extend(
        destination
    )


    print(
        "Total avant nettoyage :",
        len(events)
    )


    events = supprimer_doublons(
        events
    )


    print(
        "Après suppression doublons :",
        len(events)
    )


    creer_flux(
        events
    )


    print(
        "RSS généré avec succès"
    )



if __name__ == "__main__":

    main()
